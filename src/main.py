from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from .routes import router as expense_router


BASE_DIR = Path(__file__).resolve().parent.parent


app = FastAPI(
    title="Smart Expense Tracker API",
    description="REST API for managing personal expenses",
    version="1.0.0",
)


app.include_router(expense_router)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_file = BASE_DIR / "templates" / "index.html"
    return html_file.read_text(encoding="utf-8")