# Notes API: a CI/CD demo

A small FastAPI app with one feature (notes with a *title* and *content*, saved in Neon Postgres)
and a `/health` endpoint, plus the automation around it:

```
push code > CI checks it > merge > CD deploys that exact commit to Render > smoke test
```

* Full step-by-step guide, with every file explained: see the "Notes API: Project Structure and Code Guide" document.
* Run locally: `pip install -r requirements-dev.txt`, copy `.env.example` to `.env`, then
  `python -m app.migrate` and `uvicorn app.main:app --reload --port 8000`. Open http://localhost:8000/docs.
* Checks: `ruff check .` and `pytest -v` (needs `TEST_DATABASE_URL`, a separate Neon branch).
