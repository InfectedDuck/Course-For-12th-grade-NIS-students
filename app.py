from flask import Flask, render_template, abort, send_from_directory, make_response, request, jsonify
import json
import subprocess
import os

app = Flask(__name__)

# Load modules from JSON file
with open('modules.json', 'r', encoding='utf-8') as f:
    modules = json.load(f)

def get_module(module_id):
    """Retrieve a specific module by its ID."""
    return modules.get(str(module_id))  # Ensure the key is a string for JSON keys

def get_all_modules():
    """Retrieve all modules."""
    return modules

@app.route('/')
def home():
    response = make_response(render_template('index.html'))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/module')
def module_page():
    response = make_response(render_template('module.html', modules=get_all_modules()))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/modules/<module_id>')
def module_detail(module_id):
    module = get_module(module_id)
    if module:
        response = make_response(render_template('module_detail.html', module=module, modules=get_all_modules(), module_id=module_id))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return abort(404)

@app.route('/module/<module_id>/task/<task_id>')
def task_detail(module_id, task_id):
    with open('modules.json', 'r', encoding='utf-8') as f:
        modules = json.load(f)

    # Get the specific module and task
    module = modules.get(module_id, {})
    task = module.get('tasks', {}).get(task_id, None)

    # Check if the task exists
    if task is None:
        return "Task not found", 404

    # Ensure module_id and task_id are passed to the template
    response = make_response(render_template('task_detail.html', task=task, module=module, module_id=module_id, task_id=task_id, modules=modules))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/module/<module_id>/task/<task_id>/explanation')
def explanation(module_id, task_id):
    module = get_module(module_id)
    task = module.get('tasks', {}).get(task_id, None)
    if task and 'explanation' in task:
        explanations = task['explanation']  # Assuming explanations is a dictionary with keys for each level
        response = make_response(render_template('explanation.html', explanations=explanations, task=task, module_id=module_id, task_id=task_id, module=module, modules=modules))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    return "Explanation not found", 404

@app.route('/module/<module_id>/task/<task_id>/solution')
def solution(module_id, task_id):
    module = get_module(module_id)
    if module:
        task = module.get('tasks', {}).get(task_id, None)
        if task and 'solution' in task:
            # Pass the solution, module_id, task_id, module, and task to the template
            response = make_response(render_template(
                'solution.html', 
                solution=task['solution'], 
                module_id=module_id, 
                task_id=task_id, 
                module=module, 
                task=task
            ))
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
            return response
    return "Solution not found", 404

@app.route('/interpreter', methods=['GET', 'POST'])
def interpreter():
    if request.method == 'POST':
        code = request.json.get('code')
        try:
            # Write the code to a temporary file
            with open('temp_script.py', 'w') as f:
                f.write(code)

            # Execute the code
            result = subprocess.run(['python', 'temp_script.py'], capture_output=True, text=True)

            return jsonify({
                'stdout': result.stdout,
                'stderr': result.stderr,
                'exit_code': result.returncode
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # For GET requests, render the interpreter template
    return render_template('interpreter.html')


    # Render the interpreter page
    response = make_response(render_template('interpreter.html', module_id=module_id, task_id=task_id))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
