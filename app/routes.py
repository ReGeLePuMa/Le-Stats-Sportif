from app import webserver
from flask import request, jsonify
from app.task_runner import Task, TaskType


@webserver.before_request
def log_request_info():
    webserver.logger.info('Request: %s %s', request.method, request.url)
    webserver.logger.info('Request Headers: %s', request.headers)
    webserver.logger.info('Request Data: %s', request.get_data())

@webserver.after_request
def log_response_info(response):
    webserver.logger.info('Response: %s', response.status)
    webserver.logger.info('Response Headers: %s', response.headers)
    webserver.logger.info('Response Data: %s', response.get_data())
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
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405
    with webserver.job_counter_lock:
        if job_id and isinstance(job_id, int) and (job_id > 0 and job_id <= webserver.job_counter):
            with webserver.tasks_runner.results_lock:
                if job_id in webserver.tasks_runner.results:
                    return jsonify({"status": "done",
                                "data": webserver.tasks_runner.results[job_id]})
                return jsonify({"status": "running"})    
        return jsonify({"status": "Invalid job_id"}), 402

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405
    webserver.shutdown_event.set()
    webserver.tasks_runner.shutdown()
    return jsonify({"status": "shutting down"})

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405
    with webserver.job_counter_lock:
        job_status = []
        for i in range(1, webserver.job_counter+1):
            if i in webserver.tasks_runner.results:
                job_status.append({f"job_id_{i}": "done"})
            else:
                job_status.append({f"job_id_{i}": "running"})
        return jsonify({"status" : "done" , "data": job_status})

@webserver.route('/api/num_jobs', methods=['GET'])
def get_num_jobs():
    if request.method != 'GET':
        return jsonify({"error": "Method not allowed"}), 405
    return jsonify({"num_jobs": webserver.tasks_runner.num_jobs()})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter

    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATES_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})   

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATE_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.BEST5, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})    

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.WORST5, webserver.data_ingestor))    
    return jsonify({"job_id": curr_job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.GLOBAL_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})    

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.DIFF_FROM_MEAN_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATE_DIFF_FROM_MEAN_REQUEST, webserver.data_ingestor))    
    return jsonify({"job_id": curr_job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.MEAN_BY_CATEGORY_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})    

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    if webserver.shutdown_event.is_set():
        return jsonify({"error": "Server is shutting down"}), 503
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
        curr_job_id = webserver.job_counter
    webserver.tasks_runner.add_task(Task(curr_job_id, data, TaskType.STATE_MEAN_BY_CATEGORY_REQUEST, webserver.data_ingestor))
    return jsonify({"job_id": curr_job_id})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
