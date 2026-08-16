# Mini Calculator — Full Stack Practice Project

A small calculator app with a saved history, built specifically to
practice real git/GitHub workflow across a full stack.

## The layers

- **Frontend** (`frontend/`) — plain HTML/CSS/JS. Open `index.html`
  directly in a browser.
- **Backend / API** (`backend/`) — FastAPI. Handles calculations and
  stores each one.
- **Database** — SQLite (`calculator.db`, created automatically on
  first run). Stores calculation history.
- **Tests** (`tests/`) — pytest, tests the API directly.

## Running the backend

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```

The API will be at `http://127.0.0.1:8000`. Interactive docs (FastAPI
gives you this for free) at `http://127.0.0.1:8000/docs`.

## Running the frontend

Just open `frontend/index.html` in a browser. It calls the API running
on `127.0.0.1:8000`, so the backend needs to be running first.

## Running the tests

```bash
pytest tests/
```

## Before contributing

Read `CONTRIBUTING.md` — that's the actual workflow we're practicing
with this project, not just the code.
