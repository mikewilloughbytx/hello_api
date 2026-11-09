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
| GET    | `/haiku`   | `{"haiku": "<haiku written by Gemini>"}` |
| GET    | `/fortune` | `{"fortune": "<fortune written by Gemini>"}` |

| GET    | `/ask?q=<question>` | `{"answer": "<answer written by Gemini>"}` |

`/ask` requires a query parameter `q` of up to 200 characters. Answers are limited to about 200 output tokens and three sentences or fewer. Each valid request is a billable Gemini call.

```bash
curl "localhost:8080/ask?q=What%20is%20a%20container%3F"
```

`/haiku`, `/fortune`, and `/ask` call Gemini and return a JSON error if something goes wrong:

| Status | Meaning |
| ------ | ------- |
| 400    | `/ask` only: `q` is missing, empty, or longer than 200 characters |
| 503    | Gemini isn't set up, for example `GOOGLE_CLOUD_PROJECT` is missing or credentials can't be loaded |
| 502    | The Gemini call failed or returned no text |

The body looks like `{"error": "The Gemini request failed. Please try again later."}`. Details are written to the server log.

## Gemini setup

The Gemini endpoints use Vertex AI and Application Default Credentials. They don't use API keys or key files.

| Environment variable    | Required | Default                 |
| ----------------------- | -------- | ----------------------- |
| `GOOGLE_CLOUD_PROJECT`  | Yes      | None                    |
| `GOOGLE_CLOUD_LOCATION` | No       | `global`                |
| `GEMINI_MODEL`          | No       | `gemini-3.1-flash-lite` |

Enable Vertex AI on your Google Cloud project (billing must be linked):

```bash
gcloud services enable aiplatform.googleapis.com
```

To run locally, log in and start the app with your project ID:

```bash
gcloud auth application-default login
GOOGLE_CLOUD_PROJECT=your_project_id poetry run python main.py
```

On Cloud Run, set `GOOGLE_CLOUD_PROJECT` on the service and grant its service account the `roles/aiplatform.user` role. The `Procfile` tells Cloud Run how to start the app.

## Updating requirements.txt

`requirements.txt` is exported from Poetry. Regenerate it whenever dependencies change:

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
