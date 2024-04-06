import os
import time
import logging
from logging.handlers import RotatingFileHandler
from threading import RLock, Event
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

# Configure logging
logger = logging.getLogger(__name__)
# Create a file handler with a maximum file size of 10MB and 5 backups
handler = RotatingFileHandler('webserver.log', maxBytes=10000000, backupCount=5)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.converter = time.gmtime
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Create output directory
if not os.path.exists('results'):
    os.mkdir('results')

webserver = Flask(__name__)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.shutdown_event = Event()

webserver.job_counter = 0

# Reeentrant lock to protect the job counter and to allow the same thread to acquire the lock multiple times
webserver.job_counter_lock = RLock()

webserver.tasks_runner = ThreadPool(webserver.shutdown_event)
webserver.tasks_runner.start()

from app import routes
