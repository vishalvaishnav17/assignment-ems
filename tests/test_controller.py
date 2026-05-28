from unittest.mock import patch
from app.utils.exceptions import ValidationError, ResourceNotFoundError


@patch("app.controllers.employee_controller.employee_service")
def test_get_employees_endpoint(mock_service, client):
    """Verify GET /employees endpoint returns standard response."""
    mock_service.get_all_employees.return_value = [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "department": "HR",
            "date_joined": "2023-01-01",
        }
    ]

    response = client.get("/employees")
    assert response.status_code == 200
    assert response.json == [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "department": "HR",
            "date_joined": "2023-01-01",
        }
    ]
    mock_service.get_all_employees.assert_called_once()


@patch("app.controllers.employee_controller.employee_service")
def test_get_employee_endpoint_success(mock_service, client):
    """Verify GET /employees/<id> successfully retrieves details."""
    mock_service.get_employee_by_id.return_value = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "department": "HR",
        "date_joined": "2023-01-01",
    }

    response = client.get("/employees/1")
    assert response.status_code == 200
    assert response.json["id"] == 1
    mock_service.get_employee_by_id.assert_called_once_with(1)


@patch("app.controllers.employee_controller.employee_service")
def test_get_employee_not_found(mock_service, client):
    """Verify GET /employees/<id> returns 404 if resource does not exist."""
    mock_service.get_employee_by_id.side_effect = ResourceNotFoundError(
        "Employee with ID 99 not found."
    )

    response = client.get("/employees/99")
    assert response.status_code == 404
    assert response.json == {"error": "Employee with ID 99 not found."}


@patch("app.controllers.employee_controller.employee_service")
def test_create_employee_endpoint_success(mock_service, client):
    """Verify POST /employees endpoint successfully creates employee and returns HTTP 201."""
    payload = {
        "name": "Bob",
        "email": "bob@example.com",
        "department": "Sales",
        "date_joined": "2023-02-01",
    }
    mock_service.create_employee.return_value = {"id": 2, **payload}

    response = client.post("/employees", json=payload)
    assert response.status_code == 201
    assert response.json["id"] == 2
    mock_service.create_employee.assert_called_once_with(payload)


@patch("app.controllers.employee_controller.employee_service")
def test_create_employee_endpoint_bad_content_type(mock_service, client):
    """Verify POST /employees endpoint returns HTTP 400 when content type is not JSON."""
    response = client.post("/employees", data="not-json")
    assert response.status_code == 400
    assert "application/json" in response.json["error"]


@patch("app.controllers.employee_controller.employee_service")
def test_create_employee_endpoint_validation_error(mock_service, client):
    """Verify application ValidationErrors are mapped globally to HTTP 400."""
    payload = {
        "name": "Bob",
        "email": "invalid-email",
        "department": "Sales",
        "date_joined": "2023-02-01",
    }
    mock_service.create_employee.side_effect = ValidationError(
        "email: value is not a valid email address"
    )

    response = client.post("/employees", json=payload)
    assert response.status_code == 400
    assert response.json == {"error": "email: value is not a valid email address"}


@patch("app.controllers.employee_controller.employee_service")
def test_update_employee_endpoint_success(mock_service, client):
    """Verify PUT /employees/<id> successfully updates details."""
    payload = {"name": "Bob Dylan"}
    mock_service.update_employee.return_value = {
        "id": 2,
        "name": "Bob Dylan",
        "email": "bob@example.com",
        "department": "Sales",
        "date_joined": "2023-02-01",
    }

    response = client.put("/employees/2", json=payload)
    assert response.status_code == 200
    assert response.json["name"] == "Bob Dylan"
    mock_service.update_employee.assert_called_once_with(2, payload)


@patch("app.controllers.employee_controller.employee_service")
def test_update_employee_endpoint_bad_content_type(mock_service, client):
    """Verify PUT /employees/<id> endpoint returns HTTP 400 when content type is not JSON."""
    response = client.put("/employees/2", data="not-json")
    assert response.status_code == 400
    assert "application/json" in response.json["error"]


@patch("app.controllers.employee_controller.employee_service")
def test_delete_employee_endpoint_success(mock_service, client):
    """Verify DELETE /employees/<id> successfully removes employee."""
    response = client.delete("/employees/2")
    assert response.status_code == 200
    assert "deleted successfully" in response.json["message"]
    mock_service.delete_employee.assert_called_once_with(2)
