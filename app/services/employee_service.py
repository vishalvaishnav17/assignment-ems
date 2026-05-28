from datetime import date
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    ValidationError as PydanticValidationError,
)
from typing import Optional, List
from app.repositories.employee_repository import EmployeeRepository
from app.models.employee import Employee
from app.utils.exceptions import ValidationError, ResourceNotFoundError, ConflictError


class EmployeeCreateSchema(BaseModel):
    name: str = Field(
        ..., min_length=1, max_length=100, description="Employee full name"
    )
    email: EmailStr = Field(..., description="Unique email address")
    department: str = Field(
        ..., min_length=1, max_length=100, description="Department name"
    )
    date_joined: date = Field(..., description="Date joined in YYYY-MM-DD format")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or just whitespace.")
        return v.strip()

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Department cannot be empty or just whitespace.")
        return v.strip()


class EmployeeUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    date_joined: Optional[date] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Name cannot be empty or just whitespace.")
        return v.strip() if v is not None else None

    @field_validator("department")
    @classmethod
    def validate_department(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Department cannot be empty or just whitespace.")
        return v.strip() if v is not None else None


class EmployeeService:
    """Service layer coordinating business logic, validations, and data persistence."""

    def __init__(self, repository: EmployeeRepository | None = None):
        # Allow injecting mocked repository for unit tests
        self.repository = repository or EmployeeRepository()

    def get_all_employees(self) -> List[dict]:
        """Fetch all employees and serialize to dict list."""
        employees = self.repository.get_all()
        return [emp.to_dict() for emp in employees]

    def get_employee_by_id(self, employee_id: int) -> dict:
        """Fetch a single employee by ID and serialize, raising an error if missing."""
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found.")
        return employee.to_dict()

    def create_employee(self, data: dict) -> dict:
        """Validate input payload, check email uniqueness, create database entry."""
        try:
            validated = EmployeeCreateSchema(**data)
        except PydanticValidationError as e:
            errors = []
            for error in e.errors():
                loc = " -> ".join(str(x) for x in error["loc"])
                errors.append(f"{loc}: {error['msg']}")
            raise ValidationError("; ".join(errors))

        # Validate unique email constraint at application level
        existing = self.repository.get_by_email(validated.email)
        if existing:
            raise ConflictError(
                f"Employee with email '{validated.email}' already exists."
            )

        # Instantiate employee model and save
        employee = Employee(
            name=validated.name,
            email=validated.email,
            department=validated.department,
            date_joined=validated.date_joined,
        )
        saved = self.repository.create(employee)
        return saved.to_dict()

    def update_employee(self, employee_id: int, data: dict) -> dict:
        """Validate partial update, merge changes, save updated record."""
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found.")

        try:
            validated = EmployeeUpdateSchema(**data)
        except PydanticValidationError as e:
            errors = []
            for error in e.errors():
                loc = " -> ".join(str(x) for x in error["loc"])
                errors.append(f"{loc}: {error['msg']}")
            raise ValidationError("; ".join(errors))

        # Handle potential email changes and verify uniqueness
        if validated.email and validated.email != employee.email:
            existing = self.repository.get_by_email(validated.email)
            if existing:
                raise ConflictError(
                    f"Employee with email '{validated.email}' already exists."
                )
            employee.email = validated.email

        # Apply update operations
        if validated.name is not None:
            employee.name = validated.name
        if validated.department is not None:
            employee.department = validated.department
        if validated.date_joined is not None:
            employee.date_joined = validated.date_joined

        updated = self.repository.update(employee)
        return updated.to_dict()

    def delete_employee(self, employee_id: int) -> None:
        """Verify existence and delete employee record."""
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ResourceNotFoundError(f"Employee with ID {employee_id} not found.")
        self.repository.delete(employee)
