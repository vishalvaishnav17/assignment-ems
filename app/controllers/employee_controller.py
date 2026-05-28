from flask import Blueprint, request, jsonify
from app.services.employee_service import EmployeeService

# Create Flask Blueprint with URL prefix
employee_bp = Blueprint("employees", __name__, url_prefix="/employees")
employee_service = EmployeeService()


@employee_bp.route("", methods=["POST"])
def create_employee():
    """Create a new employee."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    payload = request.get_json()
    result = employee_service.create_employee(payload)
    return jsonify(result), 201


@employee_bp.route("", methods=["GET"])
def get_employees():
    """Retrieve all employees."""
    result = employee_service.get_all_employees()
    return jsonify(result), 200


@employee_bp.route("/<int:employee_id>", methods=["GET"])
def get_employee(employee_id: int):
    """Retrieve details for a specific employee by ID."""
    result = employee_service.get_employee_by_id(employee_id)
    return jsonify(result), 200


@employee_bp.route("/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id: int):
    """Update details for an existing employee."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    payload = request.get_json()
    result = employee_service.update_employee(employee_id, payload)
    return jsonify(result), 200


@employee_bp.route("/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id: int):
    """Delete an employee from the system."""
    employee_service.delete_employee(employee_id)
    return jsonify(
        {"message": f"Employee with ID {employee_id} deleted successfully."}
    ), 200
