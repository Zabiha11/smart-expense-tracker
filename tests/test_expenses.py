import pytest
from fastapi.testclient import TestClient

from src.main import app
from src import storage


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    storage.clear_expenses()
    
def test_create_expense():
    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Lunch"
    assert data["amount"] == 250
    assert data["category"] == "Food"
    assert data["date"] == "2026-07-31"
    
def test_get_all_expenses():
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 50,
            "category": "Transport",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["title"] == "Lunch"
    assert data[1]["title"] == "Bus"
    
def test_filter_expenses_by_category():
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 50,
            "category": "Transport",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 150,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses?category=Food")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(expense["category"] == "Food" for expense in data)

def test_category_filter_is_case_insensitive():
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses?category=food")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["category"] == "Food"
    
def test_filter_unknown_category_returns_empty_list():
    response = client.get("/expenses?category=Travel")

    assert response.status_code == 200
    assert response.json() == []
    
def test_expense_summary():
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 50,
            "category": "Transport",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 150,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    response = client.get("/expenses/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 450
    assert data["by_category"]["Food"] == 400
    assert data["by_category"]["Transport"] == 50
    
def test_monthly_summary():
    client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 50,
            "category": "Transport",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Hotel",
            "amount": 1000,
            "category": "Travel",
            "date": "2026-06-20",
        },
    )

    response = client.get(
        "/expenses/summary/monthly?year=2026&month=7"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["year"] == 2026
    assert data["month"] == 7
    assert data["total"] == 300
    assert data["transaction_count"] == 2
    assert data["by_category"]["Food"] == 250
    assert data["by_category"]["Transport"] == 50
    
    
def test_delete_expense():
    create_response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    expense_id = create_response.json()["id"]

    response = client.delete(f"/expenses/{expense_id}")

    assert response.status_code == 204

    expenses_response = client.get("/expenses")

    assert expenses_response.status_code == 200
    assert expenses_response.json() == []
    
def test_delete_nonexistent_expense():
    response = client.delete("/expenses/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Expense not found"
    
def test_negative_amount_is_rejected():
    response = client.post(
        "/expenses",
        json={
            "title": "Invalid Expense",
            "amount": -100,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 422
    
def test_zero_amount_is_rejected():
    response = client.post(
        "/expenses",
        json={
            "title": "Free Item",
            "amount": 0,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 422
    
def test_invalid_date_is_rejected():
    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "not-a-date",
        },
    )

    assert response.status_code == 422
    
def test_missing_required_fields_are_rejected():
    response = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
        },
    )

    assert response.status_code == 422
    
def test_ids_remain_unique_after_deletion():
    first = client.post(
        "/expenses",
        json={
            "title": "Lunch",
            "amount": 250,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    second = client.post(
        "/expenses",
        json={
            "title": "Bus",
            "amount": 50,
            "category": "Transport",
            "date": "2026-07-31",
        },
    )

    client.post(
        "/expenses",
        json={
            "title": "Movie",
            "amount": 300,
            "category": "Entertainment",
            "date": "2026-07-31",
        },
    )

    assert first.json()["id"] == 1
    assert second.json()["id"] == 2

    client.delete("/expenses/2")

    response = client.post(
        "/expenses",
        json={
            "title": "Coffee",
            "amount": 150,
            "category": "Food",
            "date": "2026-07-31",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 4