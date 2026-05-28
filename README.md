# Employee Management System (EMS)

Hey there! This is a simple, straightforward API to help you manage employee records. It is built using Python with Flask, SQLAlchemy, and Pydantic. 

We designed it with a clean, layered architecture so it's easy to read, maintain, and test.

## Key Features
- **Clean Structure**: Separates routes, business logic, and database operations.
- **Pydantic Validation**: Automatically checks and cleans input data.
- **Docker Ready**: Comes with Docker Compose to get you up and running with a PostgreSQL database instantly.

---

## Getting Started

### Option A: Use Docker (Recommended)
This spins up the API server and a PostgreSQL database in the background.

1. **Start everything**:
   ```bash
   docker-compose up --build -d
   ```
2. **Stop everything**:
   ```bash
   docker-compose down -v
   ```

### Option B: Run Locally
First, make sure you have [uv](https://astral.sh) installed.

1. **Install dependencies**:
   ```bash
   uv sync
   ```
2. **Run the app**:
   ```bash
   uv run python run.py
   ```
   *Note: Without a custom `.env` file, the app defaults to a local SQLite database (`ems.db`). If you want to change configurations (like ports or database URLs), just copy `.env.example` to `.env` and edit it.*

---

## Running Tests
To run all the tests and see the coverage report:
```bash
uv run python -m pytest -v --cov=app
```

---

## API Endpoints

The API runs on `http://localhost:5001`. Remember to send requests with `Content-Type: application/json`.

### 1. Create an Employee
- **POST `/employees`**
- **Request Body:**
  ```json
  {
    "name": "Shaun Murphy",
    "email": "shaun.murphy@sanjosebonaventure.org",
    "department": "Surgery",
    "date_joined": "2023-11-28"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "id": 1,
    "name": "Shaun Murphy",
    "email": "shaun.murphy@sanjosebonaventure.org",
    "department": "Surgery",
    "date_joined": "2023-11-28"
  }
  ```

### 2. Get All Employees
- **GET `/employees`**
- **Response (200 OK):**
  ```json
  [
    {
      "id": 1,
      "name": "Shaun Murphy",
      "email": "shaun.murphy@sanjosebonaventure.org",
      "department": "Surgery",
      "date_joined": "2023-11-28"
    }
  ]
  ```

### 3. Get Employee by ID
- **GET `/employees/1`**
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "name": "Shaun Murphy",
    "email": "shaun.murphy@sanjosebonaventure.org",
    "department": "Surgery",
    "date_joined": "2023-11-28"
  }
  ```

### 4. Update an Employee
- **PUT `/employees/1`**
- **Request Body:**
  ```json
  {
    "name": "Matt Murdock",
    "department": "Legal",
    "email": "matt.murdock@murdockandnelson.org",
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "id": 1,
    "name": "Matt Murdock",
    "email": "matt.murdock@murdockandnelson.org",
    "department": "Legal",
    "date_joined": "2023-11-28"
  }
  ```

### 5. Delete an Employee
- **DELETE `/employees/1`**
- **Response (200 OK):**
  ```json
  {
    "message": "Employee with ID 1 deleted successfully."
  }
  ```
