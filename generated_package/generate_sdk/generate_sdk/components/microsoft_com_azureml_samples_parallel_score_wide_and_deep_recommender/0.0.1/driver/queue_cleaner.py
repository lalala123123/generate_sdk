# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
This module provides feature to cleanup leaked queues.
"""
import traceback
from threading import Thread

import logger
from azure_queue_helper import AzureQueueHelper
from azureml_core_helper import AzuremlCoreHelper
from constant import Constant, Message
from run_context_factory import RunContextFactory


class QueueCleaner:
    """ The class for queue cleaner.
    """

    def __init__(self):
        self.logger = logger.get_logger()
        self.run_context = RunContextFactory.get_context()
        run_id = self.run_context.run_id
        self.run_id = run_id

        self.threads = []
        # Set the value to the exceptions so that the caller can know the thread stopped with error.
        self.exceptions = []

        # queue groups
        name_postfix = AzureQueueHelper.name_from_run_id(run_id)
        self.current_run_owned = [
            Constant.PENDING_TASK_QUEUE_PREFIX + name_postfix,
            Constant.PROCESSED_TASK_QUEUE_PREFIX + name_postfix,
        ]
        self.other_run_owned = []  # all queues created by this program.
        self.other_run_owned = []  # all queues created by other runs.
        self.not_owned = []  # not other_run_owned ones found in current workspace
        self.leaked = []  # other_run_owned excluding all non-terminal ones.

        self.non_terminal_name_postfix = []

        # result
        self.deleted = []  # deleted ones
        self.failed = []  # failed to delete ones

        self.azure_queue = AzureQueueHelper("")

        self.summary = ""

    def start(self):
        """ Start a thread to cleanup leaked queues."""
        self.logger.info(Message.THREAD_START.format("cleanup leaked queues"))
        thr = Thread(target=self.cleanup, args=())
        thr.start()
        self.threads.append(thr)
        self.logger.info(Message.THREAD_END.format("cleanup leaked queues"))

    def summarize(self):
        """ Write a summary of the cleanup.
        """
        self.logger.debug(
            f"Leaked: {self.leaked}, deleted : {self.deleted}, failed: {self.failed},"
            f" non terminal postfix: {self.non_terminal_name_postfix}. "
        )
        if self.leaked:
            additional = ""
            if self.deleted:
                additional += f' Deleted {", ".join(self.deleted)}.'
            if self.failed:
                additional += f' Failed to delete {", ".join(self.failed)}.'

            self.summary = Message.LEAKED_QUEUE_CLEANUP_END.format(additional)
        else:
            self.summary = Message.LEAKED_QUEUE_CLEANUP_END_NO_LEAKED_FOUND

        self.logger.info(self.summary)

    def wait(self):
        """ Wait for the cleanup thread to finish."""
        for thr in self.threads:
            try:
                thr.join()
            except BaseException as exc:
                message = Message.FAILED_TO_JOIN_THREAD.format(exc, traceback.format_exc())
                self.logger.error(message)

        self.summarize()
        self.logger.debug("All threads finished.")

    def cleanup(self):
        """ The thread target to call delete.
        """
        try:
            self.get()
            self.delete()
        except BaseException as exc:
            message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                "cleanup leaked queues", exc, traceback.format_exc()
            )
            self.logger.error(message)
            self.exceptions.append(message)

    def is_owner(self, name):
        """ A queue is considered being created by ParallelRunStep if matching the naming pattern:
            Reserved prefix + string has same len as run id.
        """
        prefix = name[:4]
        return prefix in Constant.QUEUE_PREFIXES and len(name) in [40, 60]  # prefix + uuid or sha224 hex digest

    def get(self):
        """ Get queues from the curent workspace and groups them
        """
        for que in self.azure_queue.list_queues():
            if self.is_owner(que.name):
                if que.name not in self.current_run_owned:
                    self.other_run_owned.append(que.name)
            else:
                self.not_owned.append(que.name)

        if self.other_run_owned:
            self.non_terminal_name_postfix = [
                AzureQueueHelper.name_from_run_id(run.id)
                for run in AzuremlCoreHelper().get_non_terminal_descendant_runs()
            ]

            # Consider leaked if a queue name can be mapped to a run id and the run is in terminal state.
            self.leaked = [
                name
                for name in self.other_run_owned
                if name[len(Constant.PENDING_TASK_QUEUE_PREFIX) :] not in self.non_terminal_name_postfix
            ]

    def delete(self):
        """ Delete leaked queues in current workspace.

            The queue created for task distribution is out of a run or an experiment.
            Deleting an experiment won't delete the corresponding queue.

            This Master class supports the context management protocol and delete its queue in __exit__() method.
            A queue will leak only the context management failed in rare case.
        """
        for queue_name in self.leaked:
            try:
                self.azure_queue.delete_queues([queue_name])
                self.deleted.append(queue_name)
            except BaseException as exc:
                self.failed.append(queue_name)
                message = Message.FAILED_ACTION_WITH_ERROR_DETAIL.format(
                    f"delete {queue_name}", exc, traceback.format_exc()
                )
                self.logger.warning(message)
