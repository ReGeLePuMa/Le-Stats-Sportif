from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from threading import Lock, Event

webserver = Flask(__name__)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool()

webserver.task_runner.start()

webserver.shutdown_event = Event()

webserver.job_counter = 0

webserver.job_counter_lock = Lock()

from app import routes
