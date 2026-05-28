from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    date_joined = Column(Date, nullable=False)

    def to_dict(self):
        """Serialize Employee instance to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "department": self.department,
            "date_joined": self.date_joined.isoformat() if self.date_joined else None,
        }
