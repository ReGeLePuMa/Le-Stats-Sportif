import unittest
import os
import time
import json
import sys
import requests

class TestWebserver(unittest.TestCase):
    EPSILON = 0.01
    URL = "http://127.0.0.1:5000"
    def setUp(self):
        os.system("rm -rf results/*")

    def test_states_mean_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/states_mean', json={"question": "Percent of adults aged 18 years and older who have an overweight classification"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_1', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_1.json"))
        with open("results/job_id_1.json") as f:
            my_result = json.load(f)
        with open("tests/states_mean/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_state_mean_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/state_mean', json={"question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)", "state": "Guam"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_2', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_2.json"))
        with open("results/job_id_2.json") as f:
            my_result = json.load(f)
        with open("tests/state_mean/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_best5_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/best5', json={"question": "Percent of adults aged 18 years and older who have an overweight classification"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_3', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_3.json"))
        with open("results/job_id_3.json") as f:
            my_result = json.load(f)
        with open("tests/best5/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_worst5_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/worst5', json={"question": "Percent of adults aged 18 years and older who have an overweight classification"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_4', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_4.json"))
        with open("results/job_id_4.json") as f:
            my_result = json.load(f)
        with open("tests/worst5/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_global_mean_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/global_mean', json={"question": "Percent of adults aged 18 years and older who have an overweight classification"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_5', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_5.json"))
        with open("results/job_id_5.json") as f:
            my_result = json.load(f)
        with open("tests/global_mean/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_diff_from_mean_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/diff_from_mean', json={"question": "Percent of adults aged 18 years and older who have an overweight classification"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_6', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_6.json"))
        with open("results/job_id_6.json") as f:
            my_result = json.load(f)
        with open("tests/diff_from_mean/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_state_diff_from_mean_strategy(self):
        response = requests.post(f'{TestWebserver.URL}/api/state_diff_from_mean', json={"question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Virgin Islands"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_7', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_7.json"))
        with open("results/job_id_7.json") as f:
            my_result = json.load(f)
        with open("tests/state_diff_from_mean/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_mean_by_category(self):
        response = requests.post(f'{TestWebserver.URL}/api/mean_by_category', json={"question": "Percent of adults aged 18 years and older who have an overweight classification"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_8', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_8.json"))
        with open("results/job_id_8.json") as f:
            my_result = json.load(f)
        with open("tests/mean_by_category/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)

    def test_state_mean_by_category(self):
        response = requests.post(f'{TestWebserver.URL}/api/state_mean_by_category', json={"question": "Percent of adults aged 18 years and older who have an overweight classification", "state": "Oklahoma"}, timeout=5)
        self.assertEqual(response.status_code, 200)
        time.sleep(1)
        response = requests.get(f'{TestWebserver.URL}/api/get_results/job_id_9', timeout=5)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("results/job_id_9.json"))
        with open("results/job_id_9.json") as f:
            my_result = json.load(f)
        with open("tests/state_mean_from_category/output/out-1.json") as f:
            real_result = json.load(f)
        self.assertEqual(len(my_result), len(real_result))
        self.assertListEqual(list(my_result.keys()), list(real_result.keys()))
        for key in my_result:
            self.assertAlmostEqual(my_result[key], real_result[key], delta=self.EPSILON)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        print("TestWebserver.py: Error in running the tests")
        sys.exit(1)
    print("TestWebserver.py: All tests ran successfully")
