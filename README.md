# Smart Expense Tracker API

A lightweight REST API for managing personal expenses, built with FastAPI, with a responsive web dashboard for interacting with the API.

## Features

- Create an expense
- View all expenses
- Filter expenses by category
- Calculate total expenses
- Calculate spending by category
- Calculate monthly spending
- Delete an expense
- Search expenses from the dashboard
- Category filtering
- Responsive web UI
- Interactive Swagger/OpenAPI documentation
- Automated test suite

## Tech Stack

- **Backend:** Python, FastAPI
- **Validation:** Pydantic
- **Server:** Uvicorn
- **Testing:** Pytest
- **Frontend:** HTML, CSS, JavaScript
- **Storage:** In-memory Python data structures
- **API Documentation:** OpenAPI / Swagger UI

---

## Installation

Clone the repository and navigate into the project:

```bash
git clone https://github.com/Zabiha11/smart-expense-tracker.git
cd smart-expense-tracker
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

### Activate the Virtual Environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Server

Start the FastAPI development server:

```bash
uvicorn src.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

The project includes interactive Swagger/OpenAPI documentation provided by FastAPI.

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Run Tests

Run the automated test suite using:

```bash
pytest
```

The test suite covers:

- Expense creation
- Retrieving expenses
- Category filtering
- Overall expense summaries
- Category-wise summaries
- Monthly summaries
- Input validation
- Expense deletion

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/expenses` | Create an expense |
| `GET` | `/expenses` | Get all expenses |
| `GET` | `/expenses?category=Food` | Filter expenses by category |
| `GET` | `/expenses/summary` | Get overall spending summary |
| `GET` | `/expenses/summary/monthly` | Get monthly spending summary |
| `DELETE` | `/expenses/{id}` | Delete an expense |

---

## Example Request

### Create an Expense

**POST** `/expenses`

```json
{
  "title": "Lunch",
  "amount": 250,
  "category": "Food",
  "date": "2026-08-01"
}
```

### Example Response

```json
{
  "id": 1,
  "title": "Lunch",
  "amount": 250,
  "category": "Food",
  "date": "2026-08-01"
}
```

---

## Monthly Summary

The API also provides a monthly summary endpoint.

Example:

```text
GET /expenses/summary/monthly?year=2026&month=8
```

Example response:

```json
{
  "year": 2026,
  "month": 8,
  "total": 300,
  "transaction_count": 2,
  "by_category": {
    "Food": 250,
    "Transport": 50
  }
}
```

---

## Storage

The application uses **in-memory storage**, as permitted by the assignment requirements.

No external database is required.

Expenses are stored while the application is running and are reset when the server restarts.

---

## Frontend

The project includes a lightweight web dashboard built using:

- HTML
- CSS
- JavaScript

The dashboard provides:

- Expense overview
- Total spending
- Monthly spending
- Transaction count
- Category-wise spending
- Recent expenses
- Expense search
- Category filtering
- Add expense form
- Delete expense functionality
- Responsive layout

The frontend communicates directly with the FastAPI REST API.

---

## Project Structure

```text
smart-expense-tracker/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── storage.py
│   └── ...
│
├── tests/
│   └── test_expenses.py
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── app.js
│
├── templates/
│   └── index.html
│
├── README.md
├── AI_NOTES.md
├── requirements.txt
└── .gitignore
```

---

## Testing

Run the complete automated test suite with:

```bash
pytest
```

The project currently includes automated tests covering the main API functionality.

All tests should pass before submission.

---

## Design Decisions

### FastAPI

FastAPI was selected because it provides:

- Automatic request validation through Pydantic
- Automatic OpenAPI documentation
- Simple REST API development
- Easy integration with automated testing

### In Memory Storage

The assignment explicitly allows data to be stored in memory, so an external database was intentionally avoided.

This keeps the project lightweight and easy to install and evaluate.

### Lightweight Frontend

A separate frontend framework was not introduced because the assignment focuses primarily on the REST API.

HTML, CSS, and JavaScript were used to provide a polished dashboard while keeping the application simple and easy to run.

---

## License

This project was created as part of the **Software Engineering Apprenticeship Program 2026 take home assignment**.