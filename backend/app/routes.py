import os
import json
from flask import request, jsonify
from app import webserver
from app.task_runner import Task, TaskType


# Log request and response data
@webserver.before_request
def log_request_info():
    webserver.logger.info(f'Request: {request.method} {request.url}')
    webserver.logger.info(f'Request Headers: {request.headers}')
    webserver.logger.info(f'Request Data: {request.get_data()}')

@webserver.after_request
def log_response_info(response):
    webserver.logger.info(f'Response: {response.status_code}')
    webserver.logger.info(f'Response Headers: {response.headers}')
    webserver.logger.info(f'Response Data: {response.get_data()}')
    return response

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/get_results/<job_id>', methods=['GET'])
@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    # TODO
    # Check if job_id is valid

    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })

    # If not, return running status

    # Check if method is GET
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405

    # job_id is in format "job_id_{job_id}" and have to extract the number
    try:
        job_id = int(job_id.split('_')[-1])
    except ValueError:
        return jsonify({"status": "Invalid job_id"}), 402

    # Check if job_id is valid
    if 0 < job_id <= webserver.job_counter:
        # If the job_id is in results, then it's done and we can return the result
        if job_id in webserver.tasks_runner.results:
            # Get the result
            result = webserver.tasks_runner.get_result(job_id)
            # Remove the result from the results dictionary
            webserver.tasks_runner.remove_result(job_id)
            return jsonify({"status": "done", "data": result})
        # If the job_id is in results folder, then it's done and we can return the result
        if os.path.exists(f"results/job_id_{job_id}.json"):
            with open(f"results/job_id_{job_id}.json", "r") as fin:
                try:
                    data = json.load(fin)
                    return jsonify({"status": "done", "data": data})
                # The file exists but the server didn't finish writing the result
                except json.JSONDecodeError:
                    return jsonify({"status": "running"})
        # Else, the job is still running
        return jsonify({"status": "running"})
    return jsonify({"status": "Invalid job_id"}), 402

def check_auth(username, password):
    return username == 'ReGeLePuMa' and password == 'adi@minune2k24'

# Decorator for requiring authorization
def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Authorization Required"}), 401
        return f(*args, **kwargs)
    return decorated

@webserver.route('/graceful_shutdown', methods=['GET'])
@webserver.route('/api/graceful_shutdown', methods=['GET'])
@requires_auth
def graceful_shutdown():
    # Check if method is GET
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405
    # Signal the app to stop accepting new requests
    webserver.shutdown_event.set()
    # Signal for the threadpool to finish remaining tasks and shutdown
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "shutting down"})

@webserver.route('/reset_counter', methods=['GET'])
@webserver.route('/api/reset_counter', methods=['GET'])
def reset_counter():
    # Check if method is GET
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405

    # Reset the job_counter
    with webserver.job_counter_lock:
        webserver.job_counter = 0
    return jsonify({"status": "done"})

@webserver.route('/jobs', methods=['GET'])
@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    # Check if method is GET
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405

    # Iterate through all jobs and check their status
    job_status = []
    for i in range(1, webserver.job_counter+1):
        # If the job_id is in the results dictionary or has a file in the results folder, then it's done
        if i in webserver.tasks_runner.results or os.path.exists(f"results/job_id_{i}.json"):
            job_status.append({f"job_id_{i}": "done"})
        # Else, the job is still running
        else:
            job_status.append({f"job_id_{i}": "running"})
    return jsonify({"status" : "done" , "data": job_status})

@webserver.route('/num_jobs', methods=['GET'])
@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    # Check if method is GET
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405
    return jsonify({"num_jobs": webserver.tasks_runner.num_jobs()})

@webserver.route('/states_mean', methods=['POST'])
@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATES_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/state_mean', methods=['POST'])
@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATE_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/best5', methods=['POST'])
@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.BEST5, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/worst5', methods=['POST'])
@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.WORST5, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/global_mean', methods=['POST'])
@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.GLOBAL_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/diff_from_mean', methods=['POST'])
@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.DIFF_FROM_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/state_diff_from_mean', methods=['POST'])
@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATE_DIFF_FROM_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/mean_by_category', methods=['POST'])
@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.MEAN_BY_CATEGORY_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/state_mean_by_category', methods=['POST'])
@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    # Check if method is POST
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405

    # Check if server is shutting down
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json

    # Increment job_counter atomically
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    # Add task to task queue
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATE_MEAN_BY_CATEGORY_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": f"job_id_{curr_job_id}"})

@webserver.route('/')
@webserver.route('/api')
def index():
    routes = [f"Endpoint: {rule.rule} , Methods: {','.join(rule.methods)}" for rule in webserver.url_map.iter_rules() if not rule.rule.startswith('/static')]
    return jsonify({"status" : "ok", "message": "Welcome to the API!", "routes" : routes}), 200