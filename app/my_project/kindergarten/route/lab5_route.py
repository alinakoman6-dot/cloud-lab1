from flask import Blueprint, request, jsonify
from app.my_project.kindergarten.controller.lab5_controller import Lab5Controller

lab5_bp = Blueprint('lab5_bp', __name__)
controller = Lab5Controller()

@lab5_bp.route('/insert-child', methods=['POST'])
def insert_child():
    data = request.json
    response, status = controller.insert_child(data)
    return jsonify(response), status

@lab5_bp.route('/assign-position', methods=['POST'])
def assign_position():
    data = request.json
    response, status = controller.assign_position(data)
    return jsonify(response), status

@lab5_bp.route('/generate-dummy', methods=['POST'])
def generate_dummy():
    response, status = controller.generate_dummy()
    return jsonify(response), status

@lab5_bp.route('/salary-stats', methods=['GET'])
def salary_stats():
    response, status = controller.get_salary_stats()
    return jsonify(response), status

@lab5_bp.route('/run-cursor', methods=['POST'])
def run_cursor():
    response, status = controller.run_cursor()
    return jsonify(response), status

@lab5_bp.route('/add-attendance', methods=['POST'])
def add_attendance():
    data = request.json
    response, status = controller.add_attendance(data)
    return jsonify(response), status

@lab5_bp.route('/add-parent', methods=['POST'])
def add_parent():
    response, status = controller.create_parent(request.json)
    return jsonify(response), status

@lab5_bp.route('/delete-kindergarten/<int:id>', methods=['DELETE'])
def delete_kindergarten(id):
    response, status = controller.delete_kindergarten(id)
    return jsonify(response), status

@lab5_bp.route('/delete-employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    response, status = controller.delete_employee(id)
    return jsonify(response), status

@lab5_bp.route('/audit-log', methods=['GET'])
def view_audit_log():
    return jsonify(controller.get_audit_logs()[0]), 200