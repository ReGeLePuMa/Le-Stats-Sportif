import unittest
import os
import time
import json
import random
from enum import Enum
import requests

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



class TestWebserver(unittest.TestCase):
    # Epsilon delta for real numbers comparison
    EPSILON = 0.01
    # URL of the webserver
    URL = "http://127.0.0.1:5000"
    # Endpoints of the tasks
    TASKS_ENPOINTS = {
        TaskType.STATES_MEAN_REQUEST: "/api/states_mean",
        TaskType.STATE_MEAN_REQUEST: "/api/state_mean",
        TaskType.BEST5: "/api/best5",
        TaskType.WORST5: "/api/worst5",
        TaskType.GLOBAL_MEAN_REQUEST: "/api/global_mean",
        TaskType.DIFF_FROM_MEAN_REQUEST: "/api/diff_from_mean",
        TaskType.STATE_DIFF_FROM_MEAN_REQUEST: "/api/state_diff_from_mean",
        TaskType.MEAN_BY_CATEGORY_REQUEST: "/api/mean_by_category",
        TaskType.STATE_MEAN_BY_CATEGORY_REQUEST: "/api/state_mean_by_category"
    }

    # Helper function to test a task
    def test_task(self, job_id, task_type, input_file, result_file):
        # Load the input data
        with open(input_file, "r") as f:
            data = json.load(f)
        # Send the task to the webserver
        response = requests.post(f'{TestWebserver.URL}{TestWebserver.TASKS_ENPOINTS[task_type]}', json=data, timeout=5)
        # Check if the task was accepted
        self.assertEqual(response.status_code, 200)
        # Wait for the task to finish
        time.sleep(1)
        # Check if the results are ready
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_{job_id}', timeout=5)
        self.assertEqual(response.status_code, 200)
        # Check if the file was created
        self.assertTrue(os.path.exists(f"results/job_id_{job_id}.json"))
        # Load the results for the calculation
        with open(f"results/job_id_{job_id}.json", "r") as f:
            my_result = json.load(f)
        # Load the real results
        with open(result_file, "r") as f:
            real_result = json.load(f)
        # Check if the results have the same number of entries
        self.assertEqual(len(my_result), len(real_result))
        # Check if the entries are in the same order
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        # Check if the results are the same with a delta
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=TestWebserver.EPSILON)

    # Test the states mean strategy
    def test_states_mean_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/states_mean/input")))
        self.test_task(1, TaskType.STATES_MEAN_REQUEST, f"tests/states_mean/input/in-{input_nr}.json", f"tests/states_mean/output/out-{input_nr}.json")

    # Test the state mean strategy
    def test_state_mean_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/state_mean/input")))
        self.test_task(2, TaskType.STATE_MEAN_REQUEST, f"tests/state_mean/input/in-{input_nr}.json", f"tests/state_mean/output/out-{input_nr}.json")

    # Test the best5 strategy
    def test_best5_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/best5/input")))
        self.test_task(3, TaskType.BEST5, f"tests/best5/input/in-{input_nr}.json", f"tests/best5/output/out-{input_nr}.json")

    # Test the worst5 strategy
    def test_worst5_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/worst5/input")))
        self.test_task(4, TaskType.WORST5, f"tests/worst5/input/in-{input_nr}.json", f"tests/worst5/output/out-{input_nr}.json")

    # Test the global mean strategy
    def test_global_mean_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/global_mean/input")))
        self.test_task(5, TaskType.GLOBAL_MEAN_REQUEST, f"tests/global_mean/input/in-{input_nr}.json", f"tests/global_mean/output/out-{input_nr}.json")

    # Test the diff from mean strategy
    def test_diff_from_mean_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/diff_from_mean/input")))
        self.test_task(6, TaskType.DIFF_FROM_MEAN_REQUEST, f"tests/diff_from_mean/input/in-{input_nr}.json", f"tests/diff_from_mean/output/out-{input_nr}.json")

    # Test the state diff from mean strategy
    def test_state_diff_from_mean_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/state_diff_from_mean/input")))
        self.test_task(7, TaskType.STATE_DIFF_FROM_MEAN_REQUEST, f"tests/state_diff_from_mean/input/in-{input_nr}.json", f"tests/state_diff_from_mean/output/out-{input_nr}.json")

    # Test the mean by category strategy
    def test_mean_by_category_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/mean_by_category/input")))
        self.test_task(8, TaskType.MEAN_BY_CATEGORY_REQUEST, f"tests/mean_by_category/input/in-{input_nr}.json", f"tests/mean_by_category/output/out-{input_nr}.json")

    # Test the state mean by category strategy
    def test_state_mean_by_category_strategy(self):
        # Choose a random input
        input_nr = random.randint(1,len(os.listdir("tests/state_mean_by_category/input")))
        self.test_task(9, TaskType.STATE_MEAN_BY_CATEGORY_REQUEST, f"tests/state_mean_by_category/input/in-{input_nr}.json", f"tests/state_mean_by_category/output/out-{input_nr}.json")

# Create a test suite
def test_suite():
    suite = unittest.TestSuite()
    tests = [TestWebserver(f"test_{endpoint.split('/')[-1]}_strategy") for endpoint in TestWebserver.TASKS_ENPOINTS.values()]
    suite.addTests(tests)
    return suite



if __name__ == '__main__':
    try:
        # Clear the results folder
        os.system("rm -rf results/*")
        # Reset the counter
        requests.get(f'{TestWebserver.URL}/api/reset_counter', timeout=5)
        # Run the tests
        runner = unittest.TextTestRunner()
        runner.run(test_suite())
        print("TestWebserver.py: All tests ran successfully")
    finally:
        # Clean up + reset the counter
        os.system("rm -rf results/*")
        requests.get(f'{TestWebserver.URL}/api/reset_counter', timeout=5)
