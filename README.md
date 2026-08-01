# Smart Expense Tracker API

A lightweight REST API built with **Python** and **FastAPI** for managing personal expenses. The API allows users to create, view, filter, summarize, and delete expenses while storing data locally in a JSON file.

---

## Features

- Add new expenses with automatic UUID generation
- View all recorded expenses
- Filter expenses by category
- Delete expenses by ID
- Generate expense summaries
  - Total spending
  - Category-wise totals
  - Monthly spending (`YYYY-MM`)
- Input validation using Pydantic
- Automatic interactive API documentation
- Local JSON data persistence

---

## Tech Stack

- Python 3.9+
- FastAPI
- Pydantic
- Uvicorn
- Pytest

---

## Project Structure

```text
smart-expense-tracker/
│
├── README.md
├── AI_NOTES.md
├── requirements.txt
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── storage.py
│
└── tests/
    ├── __init__.py
    └── test_api.py
```

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd smart-expense-tracker
```

### 2. Create a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

---

## Running the Application

Start the FastAPI server with:

```bash
python -m uvicorn src.main:app --reload --port 8000
```

The application will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive documentation.

| Documentation | URL |
|--------------|-----|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## Running Tests

Execute the test suite using:

```bash
python -m pytest
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/expenses` | Create a new expense |
| **GET** | `/expenses` | Retrieve all expenses |
| **GET** | `/expenses?category=Food` | Filter expenses by category |
| **GET** | `/expenses/summary` | Retrieve expense summary |
| **DELETE** | `/expenses/{expense_id}` | Delete an expense by UUID |

---

## Expense Model

```json
{
  "title": "Lunch",
  "amount": 250.50,
  "category": "Food",
  "date": "2026-08-01"
}
```

---

## Summary Response

```json
{
  "total": 4250.50,
  "category_totals": {
    "Food": 1450.50,
    "Transport": 800.00,
    "Shopping": 2000.00
  },
  "monthly_totals": {
    "2026-08": 4250.50
  }
}
```

---

## Validation Rules

- Amount must be greater than zero.
- Date must be a valid calendar date.
- Title cannot be empty.
- Category cannot be empty.
- Every expense is assigned a unique UUID.

---

## Data Storage

All expense data is stored locally in:

```text
expenses.json
```

The file is automatically created and updated whenever expenses are added or deleted.

---