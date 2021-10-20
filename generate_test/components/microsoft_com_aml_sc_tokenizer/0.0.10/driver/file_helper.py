# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides file related features.
"""
import os
from datetime import timedelta
import shutil
import time
from threading import Thread
import glob
import traceback

from constant import Message
import logger
from telemetry_logger import log_info, log_error
from time_partition_logger import TimePartitionLogger


class FileHelper:
    """ Helper to concatenate the result files into append_row_file_name for append_row jobs
    """

    TICK_SLEEP_INTERVAL = 1

    # Start a thread to log progress if exceeding this value
    SIZE_TO_START_THREAD = 1024 * 1024 * 10

    def __init__(self, args):
        self.args = args
        self.logger = logger.get_logger()
        self.overview_logger = TimePartitionLogger()

        self.folder = args.output

        self.threads = []
        self.stopping = False

        self.current_index = 0

        self.file_count = 0
        self.file_sizes = []  # in byte
        self.copied_size = 0
        self.total_size = 0

        self.from_files = None
        self.to_file = os.path.join(self.folder, f"{self.args.append_row_file_name}")
        self.init_time = time.perf_counter()
        self.start_concat_time = time.perf_counter()

        self.exceptions = []

    def analyze_source(self):
        """ Get source files
        """
        pattern = os.path.join(self.folder, f"temp_*_*_{self.args.append_row_file_name}")
        self.from_files = glob.glob(pattern)
        self.file_count = len(self.from_files)

        self.logger.debug(f"There are {self.file_count} temp files to concat: {self.from_files}.")

        # Fail the job if no temp file.
        # A job should generate temp files or should fail before this.
        if self.file_count == 0:
            message = Message.NO_SOURCE_FILE_ERROR
            self.overview_logger.flush(message)
            self.logger.error(message)
            raise Exception(message)

        for file_name in self.from_files:
            self.file_sizes.append(os.path.getsize(file_name))
        self.total_size = sum(self.file_sizes)

        if self.total_size == 0:
            self.overview_logger.flush(Message.ALL_SOURCE_FILE_ARE_EMPTY)
            self.logger.info(Message.ALL_SOURCE_FILE_ARE_EMPTY)

        msg = Message.TOTAL_FILES_TO_CONCAT.format(self.file_count, self.total_size / 1024 / 1024)
        self.logger.info(msg)
        self.overview_logger.flush(msg)

    def concat(self):
        """ Concat the temp source files into the result file."""
        # Set this to estimate copy time.
        self.start_concat_time = time.perf_counter()

        try:
            with open(self.to_file, "w") as target:
                for index, file_name in enumerate(self.from_files):
                    try:
                        self.current_index = index

                        with open(file_name, "r") as source:
                            shutil.copyfileobj(source, target)
                        target.flush()  # flush before removing the temp file
                        os.remove(file_name)

                        self.update_progress()
                    except BaseException as exc:
                        self.exceptions.append(exc)
                        msg = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                            f"Concatenate {file_name}", exc, traceback.format_exc()
                        )
                        self.overview_logger.flush(msg)
                        self.logger.error(msg)
                        raise exc
        finally:
            self.stopping = True

    def estimate_remain_seconds(self):
        """ Estimate the remain time in term of file size."""
        elapsed_seconds = time.perf_counter() - self.start_concat_time

        remain_seconds = None
        try:
            self.copied_size = os.path.getsize(self.to_file)
            if self.copied_size > 0:
                remain_seconds = elapsed_seconds * (self.total_size - self.copied_size) / self.copied_size
            return remain_seconds
        except (IOError, OSError) as exc:
            msg = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format("estimate remain time", exc, traceback.format_exc())
            self.logger.error(msg)

    def update_progress(self):
        """ Show processed files and estimated remaining time.
        """

        remain_count = self.file_count - self.current_index - 1
        if remain_count > 0:
            self.log()

    def log(self):
        """ Log progress.
        """
        elapsed_seconds = time.perf_counter() - self.start_concat_time
        remain_seconds = self.estimate_remain_seconds()
        if remain_seconds is not None:
            msg = Message.CONCAT_PROGRESS.format(
                self.current_index + 1,
                self.file_count,
                timedelta(seconds=elapsed_seconds),
                timedelta(seconds=remain_seconds),
            )
            self.logger.info(msg)
            self.overview_logger.flush(msg)

    def summarize(self):
        """ Log summary and raise exception if failed.
            If there is any exception, it will raise to end users and fail the job.
        """
        elapsed_seconds = time.perf_counter() - self.init_time

        if self.current_index == self.file_count - 1:
            msg = Message.CONCAT_FINISHED.format(self.file_count, timedelta(seconds=elapsed_seconds))
            self.overview_logger.flush(msg)
            self.logger.info(msg)
        else:
            msg = Message.CONCAT_FAILED.format(
                self.current_index + 1, self.file_count, timedelta(seconds=elapsed_seconds)
            )
            self.overview_logger.flush(msg)
            log_error(msg)

            assert self.exceptions, "There should always be exception if failed."

            raise Exception(self.exceptions)  # raise to users

    def tick(self):
        """ Write a log if it matches the log keeping criteria.
        """
        counter = 1
        try:
            while not self.stopping:
                if logger.keep(counter):
                    self.log()

                counter += 1

                time.sleep(self.TICK_SLEEP_INTERVAL)
        except BaseException as exc:
            self.exceptions.append(exc)
            msg = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format("tick", exc, traceback.format_exc())
            log_error(msg)
            # Raise exception after logging.
            # This raise won't stop the job as it is not in the main thread.
            # summarize will raise this in main thread if failed to concat all files.
            raise

    def start_tick(self):
        """ Notify users this is alive
        """
        thr = Thread(target=self.tick, args=())
        thr.start()
        self.threads.append(thr)

    def wait(self):
        """ Wait the thread to finish.
        """
        for thr in self.threads:
            thr.join()

    def start(self):
        """ The entry point to start concat.
        """
        self.analyze_source()

        if self.total_size > self.SIZE_TO_START_THREAD:
            self.start_tick()

        self.concat()
        self.wait()
        self.summarize()
