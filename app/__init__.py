from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from threading import Lock

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

webserver.job_counter_lock = Lock()

from app import routes
