from app import webserver
from flask import request, jsonify
from app.task_runner import Task, TaskType

import os
import json

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
    
    if job_id and isinstance(job_id, int) and job_id <= webserver.job_counter:
        if job_id in webserver.task_runner.results:
            return jsonify({"status": "done",
                        "data": webserver.task_runner.results[job_id]})
        return jsonify({"status": "running"})    
    return jsonify({"status": "error",}), 405

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.STATES_MEAN_REQUEST))
    return jsonify({"job_id": webserver.job_counter})   

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.STATE_MEAN_REQUEST))
    return jsonify({"job_id": webserver.job_counter})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.BEST5))
    return jsonify({"job_id": webserver.job_counter})    

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.WORST5))    
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.GLOBAL_MEAN_REQUEST))
    return jsonify({"job_id": webserver.job_counter})    

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.DIFF_FROM_MEAN_REQUEST))
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.STATE_DIFF_FROM_MEAN_REQUEST))    
    return jsonify({"job_id": webserver.job_counter})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.MEAN_BY_CATEGORY_REQUEST))
    return jsonify({"job_id": webserver.job_counter})    

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    if request.method != 'POST':
        return jsonify({"error": "Method not allowed"}), 405
    data = request.json
    with webserver.job_counter_lock:
        webserver.job_counter += 1
    webserver.task_runner.add_task(Task(webserver.job_counter, data, TaskType.STATE_MEAN_BY_CATEGORY_REQUEST))
    return jsonify({"job_id": webserver.job_counter})

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
