# Plan: FastAPI hello/goodbye API

## Context
The repo holds only `CLAUDE.md`. We need a small FastAPI app, managed with Poetry, with `GET /hello` and `GET /goodbye` returning casual JSON messages. It will later deploy to Google Cloud Run from GitHub, so it must read `PORT` (default 8080) and ship a `requirements.txt` exported from Poetry. Deployment itself is out of scope.

## Steps
1. **Branch:** `git checkout -b hello_goodbye_api` (we are on `main` and must not work there).
2. **Prompt log:** create `PROMPTS.md` at the root with a time-stamped entry for this prompt. Plan mode blocks writing it earlier, so this happens first once approved.
3. **Save plan:** copy this plan to `plans/01_hello_goodbye_api.md`.
4. **Poetry setup:** create `pyproject.toml` with `package-mode = false` (an app, not a library) and `requires-python = ">=3.12,<4.0"`. Run `poetry add fastapi uvicorn`. These are the only dependencies.
5. **`main.py`** at the root:
   - `app = FastAPI()`
   - `GET /hello` returns `{"message": "Hey there! What's up?"}`
   - `GET /goodbye` returns `{"message": "Catch you later!"}`
   - Under `if __name__ == "__main__":`, run uvicorn on host `0.0.0.0` and `int(os.environ.get("PORT", "8080"))`. Binding to `0.0.0.0` is required on Cloud Run.
6. **`requirements.txt`:** `poetry export -f requirements.txt --output requirements.txt --without-hashes`.
7. **`.gitignore`:** `.venv/`, `__pycache__/`, `*.pyc`, `.env`.
8. **`README.md`:** install (`poetry install`), run (`poetry run python main.py`), custom port (`PORT=9000 poetry run python main.py`), the endpoints with example responses, and how to regenerate `requirements.txt`.

Commits, pushes and PRs are left to you, per `CLAUDE.md`.

## Files created
`PROMPTS.md`, `plans/01_hello_goodbye_api.md`, `pyproject.toml`, `poetry.lock`, `main.py`, `requirements.txt`, `.gitignore`, `README.md`

## Verification
- Start with no `PORT` set, then `curl` `localhost:8080/hello` and `/goodbye` and confirm the JSON.
- Start with `PORT=9000` and confirm it answers on 9000.
- Confirm `requirements.txt` lists fastapi and uvicorn.
- Confirm `git status` shows the `hello_goodbye_api` branch and that `.venv` is not listed.
