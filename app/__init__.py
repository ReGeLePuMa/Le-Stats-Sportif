import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from threading import Lock, Event


logger = logging.getLogger(__name__)
handler = RotatingFileHandler('webserver.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

webserver = Flask(__name__)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.tasks_runner = ThreadPool()

webserver.tasks_runner.start()

webserver.shutdown_event = Event()

webserver.job_counter = 0

webserver.job_counter_lock = Lock()

from app import routes
