import json
import os
from queue import Queue, Empty
from threading import Thread
from enum import Enum
from .my_cache import MyCache, FullCache

class ThreadPool:
    def __init__(self, shutdown_event, cache_size=20):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        self.nr_threads = os.cpu_count() if 'TP_NUM_OF_THREADS' not in os.environ else int(os.environ['TP_NUM_OF_THREADS'])
        self.task_queue = Queue()

        # Custom class for the purpose of caching the results, based on a dictionary (job_id: result)
        self.results = MyCache(cache_size)

        self.shutdown_event = shutdown_event
        self.threads = [TaskRunner(self.task_queue, self.shutdown_event, self.results) for _ in range(self.nr_threads)]

    def start(self):
        for thread in self.threads:
            thread.start()

    def add_task(self, task):
        self.task_queue.put(task)

    def get_result(self, job_id):
        return self.results[job_id]

    def remove_result(self, job_id):
        self.results.pop(job_id)

    def shutdown(self):
        # Wait for all tasks left in the queue to be completed
        self.task_queue.join()

        for thread in self.threads:
            thread.join()

    def num_jobs(self):
        return self.task_queue.qsize()

class TaskRunner(Thread):
    def __init__(self, task_queue, shutdown_event, results):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event
        self.results = results


    def run(self):
        while True:
            try:
                # Get pending job
                # Execute the job and save the result to disk
                # Repeat until graceful_shutdown

                # Get the task from the task queue with a timeout of 1 second so that the thread can check if it can shut down
                task = self.task_queue.get(timeout=1)

                # Try putting the results in the results cache for efficiency
                try:
                    self.results[task.task_id] = task.execute()
                except FullCache:
                    continue

                # Notify the queue that the task is done
                self.task_queue.task_done()
            except Empty:
                if self.shutdown_event.is_set():
                    break

# Enum to represent the different types of tasks
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
    def __init__(self, task_id, task_data, task_type, data_ingestor):
        self.task_id = task_id
        self.task_data = task_data
        self.task_type = task_type
        self.data_ingestor = data_ingestor

    def execute(self):
        return TaskStrategy.execute_task(self)

# Strategy pattern for the execution of tasks
class TaskStrategy:
    @staticmethod
    def execute_task(task):

        # Dictionary to map the task type to the corresponding function
        strategy_functions = {
            TaskType.STATES_MEAN_REQUEST: TaskStrategy.states_mean_strategy,
            TaskType.STATE_MEAN_REQUEST: TaskStrategy.state_mean_strategy,
            TaskType.BEST5: TaskStrategy.best5_strategy,
            TaskType.WORST5: TaskStrategy.worst5_strategy,
            TaskType.GLOBAL_MEAN_REQUEST: TaskStrategy.global_mean_strategy,
            TaskType.DIFF_FROM_MEAN_REQUEST: TaskStrategy.diff_from_mean_strategy,
            TaskType.STATE_DIFF_FROM_MEAN_REQUEST: TaskStrategy.state_diff_from_mean_strategy,
            TaskType.MEAN_BY_CATEGORY_REQUEST: TaskStrategy.mean_by_category_strategy,
            TaskType.STATE_MEAN_BY_CATEGORY_REQUEST: TaskStrategy.state_mean_by_category_strategy
        }

        # Run the corresponding function based on the task type with the task's fields as arguments
        return strategy_functions[task.task_type](task.task_id, task.task_data, task.data_ingestor)

    @staticmethod
    def states_mean_strategy(id, data, data_ingestor):
        question = data['question']
        dataset, _, _ = data_ingestor.fields()

        # Pandas query to get the mean values of the question for each state
        mean_values = dataset[dataset['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values().reset_index()

        # Convert the mean values to a dictionary
        result = mean_values.set_index('LocationDesc')['Data_Value'].to_dict()

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result

    @staticmethod
    def state_mean_strategy(id, data, data_ingestor):
        question = data['question']
        state = data['state']
        dataset, _, _ = data_ingestor.fields()

        # Pandas query to get the mean value of the question for the specified state
        mean_value = dataset[(dataset['Question'] == question) & (dataset['LocationDesc'] == state)]['Data_Value'].mean()
        result = {state: mean_value}

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result

    @staticmethod
    def best5_strategy(id, data, data_ingestor):
        question = data['question']
        dataset, best_is_min, _ = data_ingestor.fields()

        #Check if the question's answer is best when it is minimum
        ok = True if question in best_is_min else False
        mean_values = dataset[dataset['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values().reset_index()
        if ok:
            # If yes, then get the first 5 rows
            mean_values = mean_values.head(5)
        else:
            # If no, then get the last 5 rows
            mean_values = mean_values.tail(5)
            # The mean values are sorted in ascending order, so we need to reverse the order
            mean_values = mean_values.iloc[::-1]

        # Convert the mean values to a dictionary
        result  = mean_values.set_index('LocationDesc')['Data_Value'].to_dict()

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result

    @staticmethod
    def worst5_strategy(id, data, data_ingestor):
        question = data['question']
        dataset, _, best_is_max = data_ingestor.fields()

        #Check if the question's answer is best when it is maximum
        ok = True if question in best_is_max else False
        mean_values = dataset[dataset['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values().reset_index()
        if ok:
            # If yes, then get the first 5 rows
            mean_values = mean_values.head(5)
        else:
            # If no, then get the last 5 rows
            mean_values = mean_values.tail(5)
            # The mean values are sorted in ascending order, so we need to reverse the order
            mean_values = mean_values.iloc[::-1]

        # Convert the mean values to a dictionary
        result  = mean_values.set_index('LocationDesc')['Data_Value'].to_dict()

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result

    @staticmethod
    def global_mean_strategy(id, data, data_ingestor):
        question = data['question']
        dataset, _, _ = data_ingestor.fields()

        # Get the mean value of the question
        mean_value = dataset[dataset['Question'] == question]['Data_Value'].mean()
        result = {"global_mean": mean_value}

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result

    @staticmethod
    def diff_from_mean_strategy(id, data, data_ingestor):
        question = data['question']
        dataset, _, _ = data_ingestor.fields()

        # Get the mean value of the question
        mean_value = dataset[dataset['Question'] == question]['Data_Value'].mean()

        # Get the mean values of the question for each state
        mean_values = dataset[dataset['Question'] == question].groupby('LocationDesc')['Data_Value'].mean().sort_values().reset_index()

        # Calculate the difference between the mean value and the mean values of the question for each state
        mean_values['diff'] = mean_value - mean_values['Data_Value']

        # Convert the differences to a dictionary
        result = mean_values.set_index('LocationDesc')['diff'].to_dict()

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result

    @staticmethod
    def state_diff_from_mean_strategy(id, data, data_ingestor):
        question = data['question']
        state = data['state']
        dataset, _, _ = data_ingestor.fields()

        # Get the mean value of the question
        mean_value = dataset[dataset['Question'] == question]['Data_Value'].mean()

        # Get the mean value of the question for the specified state
        mean_value_state = dataset[(dataset['Question'] == question) & (dataset['LocationDesc'] == state)]['Data_Value'].mean()

        # Write the result to a json file
        with open(f'results/job_id_{id}.json', 'w') as f:
            json.dump({state: mean_value - mean_value_state}, f)

        # Return the non-json result
        return {state: mean_value - mean_value_state}

    @staticmethod
    def mean_by_category_strategy(id, data, data_ingestor):
        question = data['question']
        dataset, _, _ = data_ingestor.fields()

        # Get the mean values of the question for each state, category, and segment
        mean_values = dataset[dataset['Question'] == question].groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value'].mean().reset_index()

        # Convert the mean values to a dictionary
        result_dict = {}
        for _, row in mean_values.iterrows():
            # The format of dictionary is {(state, category, segment) : mean_value}
            state = row['LocationDesc']
            category = row['StratificationCategory1']
            segment = row['Stratification1']
            mean_value = row['Data_Value']
            key = str((state, category, segment))
            result_dict[key] = mean_value

        # Write the result to a json file
        with open(f"results/job_id_{id}.json", 'w') as f:
            json.dump(result_dict, f)

        # Return the non-json result
        return result_dict

    @staticmethod
    def state_mean_by_category_strategy(id, data, data_ingestor):
        question = data['question']
        state = data['state']
        dataset, _, _ = data_ingestor.fields()

        # Get the mean values of the question for each category and segment for the specified state
        mean_values = dataset[(dataset['Question'] == question) & (dataset['LocationDesc'] == state)].groupby(['StratificationCategory1', 'Stratification1'])['Data_Value'].mean().reset_index()

        # Convert the mean values to a dictionary
        result_dict = {}
        for _, row in mean_values.iterrows():
            # The format of dictionary is {(category, segment) : mean_value}
            category = row['StratificationCategory1']
            segment = row['Stratification1']
            mean_value = row['Data_Value']
            key = str((category, segment))
            result_dict[key] = mean_value

        result = {state: result_dict}

        # Write the result to a json file
        with open(f"results/job_id_{id}.json", 'w') as f:
            json.dump(result, f)

        # Return the non-json result
        return result