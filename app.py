from flask import Flask, render_template, jsonify, abort, send_from_directory
import json

app = Flask(__name__)

with open('modules.json') as f:
    modules = json.load(f)

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/module')
def module_page():
    return render_template('module.html', modules=modules)

@app.route('/modules/<module_id>')
def module_detail(module_id):
    module = modules.get(module_id)
    if module:
        return render_template('module_detail.html', module=module, modules=modules, module_id=module_id)
    return abort(404)

@app.route('/modules/<module_id>/tasks')
def get_tasks(module_id):
    module = modules.get(module_id)
    if module:
        tasks = module.get("tasks", {})
        return jsonify(tasks)
    return jsonify({"error": "Module not found"}), 404

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
