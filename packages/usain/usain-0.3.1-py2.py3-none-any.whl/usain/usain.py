# -*- coding: utf-8 -*-
from loguru import logger
import threading
import multiprocessing as mp

import datetime
import time


"""Main module."""


class Task:
    def __init__(self, name, pipe, init_data=None, daemon=True):
        """Create new task."""
        self.name = name
        self.unique_id = self.name + str(id(self))
        self.status = "stopped"
        self._init_data = init_data
        self._pipeline = pipe
        self.daemon = daemon

    def __str__(self):
        return "Task: {name} is {status}".format(name=self.name, status=self.status)

    def _run(self):
        if self._init_data is None:
            logger.info(
                "Running pipeline for task {} without initial data".format(self.name)
            )
            logger.debug(
                "Task {} running at node 1 out of {}".format(
                    self.name, len(self._pipeline)
                )
            )
            res = self._pipeline[0]()
        else:
            logger.info(
                "Running pipeline for task {} with initial data".format(self.name)
            )
            logger.debug(
                "Task {} running at node 1 out of {}".format(
                    self.name, len(self._pipeline)
                )
            )
            res = self._pipeline[0](self._init_data)
        for idx, fn in enumerate(self._pipeline[1:]):
            logger.debug(
                "Task {} running at node {} out of {}".format(
                    self.name, idx + 2, len(self._pipeline)
                )
            )
            res = fn(res)

    def run(self):
        """Run the pipeline on the data."""
        if self.daemon:
            job_thread = threading.Thread(target=self._run)
            job_thread.start()
        else:
            self._run()


class Runner:
    def __init__(self, name="Native Runner", daemon=True):
        self.name = name
        self.status = "stopped"
        self._agenda, self._tasks, self._taskstimes = {}, {}, {}
        self.daemon = True

    def add(self, task, seconds):
        self._agenda[task.unique_id] = seconds
        self._taskstimes[task.unique_id] = seconds
        self._tasks[task.unique_id] = task

    def _run_pending(self):
        while 1:
            for k, v in self._agenda.items():
                if v == 0:
                    self._tasks[k].daemon = True
                    self._tasks[k].run()
                    self._agenda[k] = self._taskstimes[k]
                else:
                    self._agenda[k] -= 1

            time.sleep(1)

    def _background_worker(self):
        workerThread = threading.Thread(target=self._run_pending)
        workerThread.start()

    def run(self):
        if self.daemon:
            self._background_worker()
        else:
            self._run_pending()
