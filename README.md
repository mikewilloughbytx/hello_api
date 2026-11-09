# hello_api

A small FastAPI app that says hello and goodbye.

## Install

You need Python 3.12 or newer and [Poetry](https://python-poetry.org/).

```bash
poetry install
```

## Run

```bash
poetry run python main.py
```

The app listens on port 8080 by default. To use another port, set `PORT`:

```bash
PORT=9000 poetry run python main.py
```

## Endpoints

| Method | Path       | Response                                |
| ------ | ---------- | --------------------------------------- |
| GET    | `/hello`   | `{"message": "Hey there! What's up?"}`  |
| GET    | `/goodbye` | `{"message": "Catch you later!"}`       |

## Updating requirements.txt

`requirements.txt` is exported from Poetry. Regenerate it whenever dependencies change:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
