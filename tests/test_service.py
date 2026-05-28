from datetime import date
from unittest.mock import MagicMock

import pytest

from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.utils.exceptions import ConflictError, ResourceNotFoundError, ValidationError


def test_get_all_employees():
    """Verify that get_all_employees returns all records properly serialized."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    emp1 = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="HR",
        date_joined=date(2023, 1, 1),
    )
    emp2 = Employee(
        id=2,
        name="Bob",
        email="bob@example.com",
        department="IT",
        date_joined=date(2023, 2, 1),
    )
    mock_repo.get_all.return_value = [emp1, emp2]

    service = EmployeeService(repository=mock_repo)
    result = service.get_all_employees()

    assert len(result) == 2
    assert result[0]["name"] == "Alice"
    assert result[1]["name"] == "Bob"
    mock_repo.get_all.assert_called_once()


def test_get_employee_by_id_success():
    """Verify that an employee can be successfully retrieved and serialized."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    emp = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="HR",
        date_joined=date(2023, 1, 1),
    )
    mock_repo.get_by_id.return_value = emp

    service = EmployeeService(repository=mock_repo)
    result = service.get_employee_by_id(1)

    assert result["id"] == 1
    assert result["name"] == "Alice"
    mock_repo.get_by_id.assert_called_once_with(1)


def test_get_employee_by_id_not_found():
    """Verify that a ResourceNotFoundError is raised if the employee ID does not exist."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    mock_repo.get_by_id.return_value = None

    service = EmployeeService(repository=mock_repo)
    with pytest.raises(ResourceNotFoundError) as excinfo:
        service.get_employee_by_id(99)
    assert "Employee with ID 99 not found" in str(excinfo.value)
    mock_repo.get_by_id.assert_called_once_with(99)


def test_create_employee_success():
    """Verify successful employee creation through the service layer with correct validation."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    mock_repo.get_by_email.return_value = None

    def mock_create(emp):
        emp.id = 1
        return emp

    mock_repo.create.side_effect = mock_create

    service = EmployeeService(repository=mock_repo)
    payload = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "department": "Marketing",
        "date_joined": "2023-01-15",
    }

    result = service.create_employee(payload)
    assert result["id"] == 1
    assert result["name"] == "Alice Smith"
    assert result["email"] == "alice@example.com"
    mock_repo.get_by_email.assert_called_once_with("alice@example.com")
    mock_repo.create.assert_called_once()


def test_create_employee_validation_failure():
    """Verify that validation errors are correctly caught and raised."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    service = EmployeeService(repository=mock_repo)

    # Scenario 1: Missing email
    payload_missing_email = {
        "name": "Alice Smith",
        "department": "Marketing",
        "date_joined": "2023-01-15",
    }
    with pytest.raises(ValidationError) as excinfo:
        service.create_employee(payload_missing_email)
    assert "email" in str(excinfo.value)

    # Scenario 2: Invalid date format
    payload_invalid_date = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "department": "Marketing",
        "date_joined": "not-a-date",
    }
    with pytest.raises(ValidationError) as excinfo:
        service.create_employee(payload_invalid_date)
    assert "date_joined" in str(excinfo.value)

    # Scenario 3: Empty name
    payload_empty_name = {
        "name": "   ",
        "email": "alice@example.com",
        "department": "Marketing",
        "date_joined": "2023-01-15",
    }
    with pytest.raises(ValidationError) as excinfo:
        service.create_employee(payload_empty_name)
    assert "Name cannot be empty" in str(excinfo.value)


def test_create_employee_duplicate_email():
    """Verify email uniqueness validation checks."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    mock_repo.get_by_email.return_value = MagicMock()

    service = EmployeeService(repository=mock_repo)
    payload = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "department": "Marketing",
        "date_joined": "2023-01-15",
    }

    with pytest.raises(ConflictError) as excinfo:
        service.create_employee(payload)
    assert "already exists" in str(excinfo.value)


def test_update_employee_success():
    """Verify that an employee can be successfully updated with partial fields."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    emp = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="HR",
        date_joined=date(2023, 1, 1),
    )
    mock_repo.get_by_id.return_value = emp
    mock_repo.get_by_email.return_value = None
    mock_repo.update.return_value = emp

    service = EmployeeService(repository=mock_repo)
    payload = {
        "name": "Alice Cooper",
        "email": "alice.cooper@example.com",
        "department": "Engineering",
    }

    result = service.update_employee(1, payload)

    assert result["name"] == "Alice Cooper"
    assert result["email"] == "alice.cooper@example.com"
    assert result["department"] == "Engineering"
    assert result["date_joined"] == "2023-01-01"  # Unchanged
    mock_repo.update.assert_called_once_with(emp)


def test_update_employee_not_found():
    """Verify update raises ResourceNotFoundError if employee does not exist."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    mock_repo.get_by_id.return_value = None

    service = EmployeeService(repository=mock_repo)
    with pytest.raises(ResourceNotFoundError) as excinfo:
        service.update_employee(99, {"name": "Bob"})
    assert "Employee with ID 99 not found" in str(excinfo.value)


def test_update_employee_validation_failure():
    """Verify update raises ValidationError if update inputs are invalid."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    emp = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="HR",
        date_joined=date(2023, 1, 1),
    )
    mock_repo.get_by_id.return_value = emp

    service = EmployeeService(repository=mock_repo)
    with pytest.raises(ValidationError) as excinfo:
        service.update_employee(1, {"name": "   "})
    assert "Name cannot be empty" in str(excinfo.value)


def test_update_employee_conflict_email():
    """Verify update raises ConflictError if update email belongs to another employee."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    emp = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="HR",
        date_joined=date(2023, 1, 1),
    )
    mock_repo.get_by_id.return_value = emp

    # Simulate another employee already using the new email
    another_emp = Employee(
        id=2,
        name="Bob",
        email="bob@example.com",
        department="IT",
        date_joined=date(2023, 1, 1),
    )
    mock_repo.get_by_email.return_value = another_emp

    service = EmployeeService(repository=mock_repo)
    with pytest.raises(ConflictError) as excinfo:
        service.update_employee(1, {"email": "bob@example.com"})
    assert "already exists" in str(excinfo.value)


def test_delete_employee_success():
    """Verify successful employee deletion."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    emp = Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="HR",
        date_joined=date(2023, 1, 1),
    )
    mock_repo.get_by_id.return_value = emp

    service = EmployeeService(repository=mock_repo)
    service.delete_employee(1)

    mock_repo.delete.assert_called_once_with(emp)


def test_delete_employee_not_found():
    """Verify delete raises ResourceNotFoundError if employee does not exist."""
    mock_repo = MagicMock(spec=EmployeeRepository)
    mock_repo.get_by_id.return_value = None

    service = EmployeeService(repository=mock_repo)
    with pytest.raises(ResourceNotFoundError) as excinfo:
        service.delete_employee(99)
    assert "Employee with ID 99 not found" in str(excinfo.value)
