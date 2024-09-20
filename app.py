from flask import Flask, render_template, abort, send_from_directory, make_response
import json

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
    
    response = make_response(render_template('task_detail.html', task=task, module=module, modules=modules))
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
