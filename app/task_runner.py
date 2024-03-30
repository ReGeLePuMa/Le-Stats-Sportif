from queue import Queue
from threading import Thread, Event, Lock
from enum import Enum
import time
import os

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.nr_threads = os.cpu_count() if 'TP_NUM_OF THREADS' not in os.environ else int(os.environ['TP_NUM_OF THREADS'])
        self.task_queue = Queue()
        self.results = {}
        self.results_lock = Lock()
        self.shutdown_event = Event()
        self.threads = [TaskRunner(self.task_queue, self.shutdown_event) for _ in range(self.nr_threads)]

    def start(self):
        for thread in self.threads:
            thread.start()

    def add_task(self, task):
        self.task_queue.put(task)

    def shutdown(self):
        self.shutdown_event.set()
        for thread in self.threads:
            thread.join()                
        

class TaskRunner(Thread):
    def __init__(self, task_queue, shutdown_event):
        super().__init__()
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event
        

    def run(self):
        while True:
            # Get pending job
            # Execute the job and save the result to disk
            # Repeat until graceful_shutdown
            if self.shutdown_event.is_set():
                break
            task = self.task_queue.get()
            with self.results_lock:
                self.results[task.task_id] = task.execute()
            self.task_queue.task_done()


class TaskType(Enum):
    STATES_MEAN_REQUEST = 1
    STATE_MEAN_REQUEST = 2
    BEST5 = 3
    WORST5 = 4
    GLOBAL_MEAN_REQUEST = 5
    DIFF_FROM_MEAN_REQUEST = 6
    STATE_DIFF_FROM_MEAN_REQUEST = 7
    MEAN_BY_CATEGORY_REQUEST = 8
    STATE_MEAN_BY_CATEGORY_REQUEST = 9


class Task:
    def __init__(self, task_id, task_data, task_type):
        self.task_id = task_id
        self.task_data = task_data
        self.task_type = task_type

    def execute(self):
        return TaskStrategy.execute_task(self)

class TaskStrategy:
    @staticmethod
    def execute_task(task):
        strategy_functions = {
            TaskType.STATES_MEAN_REQUEST: states_mean_strategy,
            TaskType.STATE_MEAN_REQUEST: state_mean_strategy,
            TaskType.BEST5: best5_strategy,
            TaskType.WORST5: worst5_strategy,
            TaskType.GLOBAL_MEAN_REQUEST: global_mean_strategy,
            TaskType.DIFF_FROM_MEAN_REQUEST: diff_from_mean_strategy,
            TaskType.STATE_DIFF_FROM_MEAN_REQUEST: state_diff_from_mean_strategy,
            TaskType.MEAN_BY_CATEGORY_REQUEST: mean_by_category_strategy,
            TaskType.STATE_MEAN_BY_CATEGORY_REQUEST: state_mean_by_category_strategy
        }
        return strategy_functions[task.task_type](task.task_data)
    
def states_mean_strategy(data):
    pass

def state_mean_strategy(data):
    pass

def best5_strategy(data):
    pass

def worst5_strategy(data):
    pass

def global_mean_strategy(data):
    pass

def diff_from_mean_strategy(data):
    pass

def state_diff_from_mean_strategy(data):
    pass

def mean_by_category_strategy(data):
    pass


def state_mean_by_category_strategy(data):
    pass  