from app.database import db_session
from app.models.employee import Employee
from typing import List, Optional


class EmployeeRepository:
    """Repository layer responsible for CRUD operations on the employees table."""

    def get_all(self) -> List[Employee]:
        """Retrieve all employees from the database."""
        return db_session.query(Employee).all()

    def get_by_id(self, employee_id: int) -> Optional[Employee]:
        """Retrieve an employee by their ID."""
        return db_session.query(Employee).filter(Employee.id == employee_id).first()

    def get_by_email(self, email: str) -> Optional[Employee]:
        """Retrieve an employee by their unique email."""
        return db_session.query(Employee).filter(Employee.email == email).first()

    def create(self, employee: Employee) -> Employee:
        """Insert a new employee record and commit transaction."""
        db_session.add(employee)
        db_session.commit()
        return employee

    def update(self, employee: Employee) -> Employee:
        """Commit the changes made to the employee record."""
        db_session.commit()
        return employee

    def delete(self, employee: Employee) -> None:
        """Remove the employee record and commit transaction."""
        db_session.delete(employee)
        db_session.commit()
