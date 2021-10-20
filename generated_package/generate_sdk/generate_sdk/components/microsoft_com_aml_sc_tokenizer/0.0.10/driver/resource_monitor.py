# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides performance monitoring related features.
"""
import os
import csv
import time
import threading
from threading import Thread
from multiprocessing import current_process
from abc import ABC, abstractclassmethod
import psutil

import utility
import logger
from log_config import LogConfig


class ResourceMonitor(object):
    """ The class for system and process resource usage monitoring.
        It will start a standalone thread to monitor resouce usage of
        container and resource usage of process which ResourceMonitor located.
        Resource usage: CPU, GPU, MEMORY, DISK, NETWORK
    """

    SLEEP_BEFORE_NEXT_POLL = 60  # The time to sleep before next poll

    class MetricWriter(ABC):
        """ Abstract class for metric writer."""

        def __init__(self, file):
            self.file = file

        @abstractclassmethod
        def write(cls, metrics: dict):
            """ Write metrics to file."""

        def ensure_saved(self):
            """ Flush the cache."""
            self.file.flush()

    class CsvMetricWriter(MetricWriter):
        """ Writer to csv file."""

        def __init__(self, file):
            self.is_header_exist = False
            self.csv_writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            super().__init__(file)

        def write(self, metrics: dict):
            if not self.is_header_exist:
                self.is_header_exist = True
                self.csv_writer.writerow(list(metrics.keys()))
            self.csv_writer.writerow(list(metrics.values()))

    class Metrics(ABC):
        """ Abstract class for metrics."""

        def __init__(self, writer):
            self.writer = writer
            self.logger = logger.get_logger(name="Metrics")

        @abstractclassmethod
        def _poll(cls):
            """ Poll the metrics."""

        def collect(self):
            """ collect and save metrics."""
            metrics = self._poll()
            self.writer.write(metrics)
            self.writer.ensure_saved()
            self.logger.debug(f"Metrics collected: {metrics}")

    class SysMetrics(Metrics):
        """ The class provides features to write sys metrics."""

        def _poll(self):
            metrics = {}
            metrics["TIME_STAMP"] = utility.fmt_time(utility.timestamp())
            cpu_percent = psutil.cpu_percent()
            metrics["CPU_PERCENT"] = cpu_percent

            vmem = psutil.virtual_memory()
            metrics["MEMORY_TOTAL"] = vmem.total
            metrics["MEMORY_AVAILABLE"] = vmem.available
            metrics["MEMORY_USED"] = vmem.used
            metrics["MEMORY_USED_PERCENT"] = vmem.percent

            disk = psutil.disk_io_counters()
            metrics["DISK_IO_READ_COUNT"] = disk.read_count
            metrics["DISK_IO_WRITE_COUNT"] = disk.write_count
            metrics["DISK_IO_READ_BYTES"] = disk.read_bytes
            metrics["DISK_IO_WRITE_BYTES"] = disk.write_bytes

            network = psutil.net_io_counters()
            metrics["NETWORK_BYTES_SENT"] = network.bytes_sent
            metrics["NETWORK_BYTES_RECV"] = network.bytes_recv

            """ TODO: Comments out GPU part since SDK now is not installing nvidia-ml-py3.
            Will enable it after SDK ready.
            if os.environ.get('AZ_BATCHAI_NUM_GPUS') is not None:
                gpu_count = int(os.environ['AZ_BATCHAI_NUM_GPUS'])
                if gpu_count > 0:
                    import nvidia_smi #pip install nvidia-ml-py3
                    for i in range(gpu_count):
                        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
                        res = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
                        metrics[f'GPU_{i}_USAGE'] = res.gpu
                        metrics[f'GPU_{i}_MEM_USAGE'] = res.memory"""
            return metrics

    class ProcessMetrics(Metrics):
        """ The class provides features to write process metrics."""

        CPU_PERCENT_INTERVAL = 1

        def _poll(self):
            metrics = {}
            metrics["TIME_STAMP"] = utility.fmt_time(utility.timestamp())
            process = psutil.Process(os.getpid())
            cpu_percent = process.cpu_percent(interval=self.CPU_PERCENT_INTERVAL)
            metrics["CPU_PERCENT"] = cpu_percent

            cpu_times = process.cpu_times()
            metrics["CPU_TIMES_USER"] = cpu_times.user
            metrics["CPU_TIMES_SYSTEM"] = cpu_times.system

            mem = process.memory_percent()
            metrics["MEMORY_PERCENT"] = mem

            disk = process.io_counters()
            metrics["DISK_IO_READ_COUNT"] = disk.read_count
            metrics["DISK_IO_WRITE_COUNT"] = disk.write_count
            metrics["DISK_IO_READ_BYTES"] = disk.read_bytes
            metrics["DISK_IO_WRITE_BYTES"] = disk.write_bytes

            thread_num = process.num_threads()
            metrics["THREAD_NUM"] = thread_num

            return metrics

    class _ResourceMonitor(object):
        """ The class provides features to monitor resource usage."""

        def __init__(self, interval):
            self.interval = interval
            self.logger = logger.get_logger(name="ResourceMonitor")
            ip_addr = utility.get_ip()
            self.dir = os.path.join(LogConfig().log_dir, "sys/perf", ip_addr)
            os.makedirs(self.dir, exist_ok=True)

            self.monitor_enable = True
            self.monitor_thread = Thread(target=self.poll_metrics, args=())

            self.logger.info(f"Resource monitor init with interval={interval}s.")

        def start(self):
            """ Start the monitor thread."""
            self.monitor_thread.start()

        def poll_metrics(self):
            """ Poll the metrics."""
            pid = os.getpid()
            tid = threading.get_ident()

            sys_resource_monitor_file = os.path.join(self.dir, f"sys.csv")

            sys_mo_exist = False
            if os.path.exists(sys_resource_monitor_file):
                sys_mo_exist = True

            process_resource_monitor_file = os.path.join(self.dir, f"{current_process().name}.csv")

            with open(sys_resource_monitor_file, "a", newline="") as sys_f, open(
                process_resource_monitor_file, "a", newline=""
            ) as process_f:
                monitor_metrics = []
                if not sys_mo_exist:
                    monitor_metrics.append(ResourceMonitor.SysMetrics(ResourceMonitor.CsvMetricWriter(sys_f)))
                monitor_metrics.append(ResourceMonitor.ProcessMetrics(ResourceMonitor.CsvMetricWriter(process_f)))

                self.logger.info(f"Resource monitor tid = {tid} started for process pid={pid}.")
                while self.monitor_enable:
                    for metrics in monitor_metrics:
                        metrics.collect()
                        self.logger.debug(f"Metrics collected for process pid={pid}.")
                    time.sleep(self.interval)

            self.logger.info(f"Resource monitor tid = {tid} quit")

    _instance = None

    def __init__(self, interval=60):
        if not ResourceMonitor._instance:
            ResourceMonitor._instance = ResourceMonitor._ResourceMonitor(interval)
        else:
            raise Exception(f"Resource monitor has been initialized, interval={ResourceMonitor._instance.interval}s")

    def __enter__(self):
        ResourceMonitor._instance.start()

    def __exit__(self, exception_type, exception_value, traceback):
        ResourceMonitor._instance.monitor_enable = False
        ResourceMonitor._instance.monitor_thread.join()
