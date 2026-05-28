from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from datetime import date


def test_create_and_get_employee():
    """Verify that an employee can be created and retrieved from the database."""
    repo = EmployeeRepository()

    emp = Employee(
        name="John Doe",
        email="john.doe@example.com",
        department="Engineering",
        date_joined=date(2023, 5, 1),
    )

    created = repo.create(emp)
    assert created.id is not None
    assert created.name == "John Doe"

    # Retrieve by ID
    retrieved = repo.get_by_id(created.id)
    assert retrieved is not None
    assert retrieved.email == "john.doe@example.com"

    # Retrieve by email
    retrieved_by_email = repo.get_by_email("john.doe@example.com")
    assert retrieved_by_email is not None
    assert retrieved_by_email.id == created.id


def test_update_employee():
    """Verify that updates to employee records are properly persisted."""
    repo = EmployeeRepository()
    emp = Employee(
        name="Jane Smith",
        email="jane.smith@example.com",
        department="HR",
        date_joined=date(2022, 10, 15),
    )
    repo.create(emp)

    emp.name = "Jane Doe"
    updated = repo.update(emp)
    assert updated.name == "Jane Doe"

    retrieved = repo.get_by_id(emp.id)
    assert retrieved.name == "Jane Doe"


def test_delete_employee():
    """Verify that employees can be successfully deleted from the database."""
    repo = EmployeeRepository()
    emp = Employee(
        name="Bob Johnson",
        email="bob@example.com",
        department="Sales",
        date_joined=date(2021, 1, 1),
    )
    repo.create(emp)

    repo.delete(emp)

    assert repo.get_by_id(emp.id) is None
