import pytest
from fastapi.testclient import TestClient
from src.main import app, storage


@pytest.fixture(autouse=True)
def reset_storage():
    """Reset storage before each test to ensure test isolation."""
    storage.filepath = None  # Disable file persistence during tests
    storage.expenses.clear()


client = TestClient(app)


def test_create_expense():
    payload = {
        "title": "Groceries",
        "amount": 45.50,
        "category": "Food",
        "date": "2026-08-01",
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Groceries"
    assert data["amount"] == 45.50
    assert "id" in data


def test_invalid_expense_amount():
    payload = {
        "title": "Invalid Expense",
        "amount": -10.0,
        "category": "Misc",
        "date": "2026-08-01",
    }
    response = client.post("/expenses", json=payload)
    assert response.status_code == 422  # Validation Error


def test_list_and_filter_expenses():
    client.post("/expenses", json={"title": "Lunch", "amount": 15.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Bus Ticket", "amount": 3.0, "category": "Transport", "date": "2026-08-01"})

    # Fetch all
    response = client.get("/expenses")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Filter by category
    response_filter = client.get("/expenses?category=Food")
    assert response_filter.status_code == 200
    assert len(response_filter.json()) == 1
    assert response_filter.json()[0]["title"] == "Lunch"


def test_get_summary():
    client.post("/expenses", json={"title": "Lunch", "amount": 15.0, "category": "Food", "date": "2026-08-01"})
    client.post("/expenses", json={"title": "Dinner", "amount": 25.0, "category": "Food", "date": "2026-08-02"})
    client.post("/expenses", json={"title": "Taxi", "amount": 10.0, "category": "Transport", "date": "2026-07-15"})

    response = client.get("/expenses/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 50.0
    assert data["total_count"] == 3
    assert data["by_category"]["Food"] == 40.0
    assert data["by_category"]["Transport"] == 10.0
    assert data["monthly_summary"]["2026-08"] == 40.0
    assert data["monthly_summary"]["2026-07"] == 10.0


def test_delete_expense():
    create_res = client.post("/expenses", json={"title": "Coffee", "amount": 4.5, "category": "Food", "date": "2026-08-01"})
    expense_id = create_res.json()["id"]

    # Delete existing
    del_res = client.delete(f"/expenses/{expense_id}")
    assert del_res.status_code == 204

    # Verify deletion
    list_res = client.get("/expenses")
    assert len(list_res.json()) == 0

    # Delete non-existing
    del_again = client.delete(f"/expenses/{expense_id}")
    assert del_again.status_code == 404