# Smart Expense Tracker API

A lightweight REST API built with Python and FastAPI to manage personal expenses, perform category filtering, and compute real-time expense aggregations.

## Features

- **Expense Management:** Add, view, filter, and delete personal expenses with UUID identification.
- **Data Validation:** Enforces positive monetary amounts, valid calendar dates, and required string constraints.
- **Aggregations & Summaries:** Calculates total expense amounts, per-category subtotals, and monthly breakdowns (`YYYY-MM`).
- **Interactive Documentation:** Built-in OpenAPI / Swagger UI support at `/docs`.
- **JSON Persistence:** Persists data locally to `expenses.json` across server restarts.

---

## Directory Structure

```text
smart-expense-tracker/
├── README.md          # Project overview, installation, and usage
├── AI_NOTES.md         # AI collaboration and engineering decisions
├── requirements.txt    # Project dependencies
├── src/
│   ├── __init__.py     # Package initializer
│   ├── main.py         # FastAPI route handlers & app initialization
│   ├── models.py       # Pydantic schemas & field validations
│   └── storage.py      # Persistence and aggregation logic
└── tests/
    ├── __init__.py     # Test package initializer
    └── test_api.py     # Automated API test suite

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
