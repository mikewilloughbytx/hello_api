import logging
import os
from functools import lru_cache

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google import genai
from google.auth.exceptions import DefaultCredentialsError
from google.genai import types

logger = logging.getLogger(__name__)

HAIKU_PROMPT = (
    "Write a short haiku about DevOps. Reply with only the haiku, with no title."
)
FORTUNE_PROMPT = (
    "Write a one-sentence, software-themed fortune-cookie message. "
    "Reply with only the message."
)
MAX_OUTPUT_TOKENS = 100
GEMINI_TIMEOUT_MS = 30_000

app = FastAPI()


class GeminiError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.message = message


@app.exception_handler(GeminiError)
def handle_gemini_error(request: Request, exc: GeminiError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"error": exc.message})


# lru_cache does not store exceptions, so a failed setup is retried on the next request.
@lru_cache(maxsize=1)
def get_client() -> genai.Client:
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project:
        raise GeminiError(503, "Gemini is not configured: GOOGLE_CLOUD_PROJECT is not set.")
    try:
        return genai.Client(
            vertexai=True,
            project=project,
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "global"),
            http_options=types.HttpOptions(timeout=GEMINI_TIMEOUT_MS),
        )
    except Exception as exc:
        logger.exception("Could not create the Gemini client")
        raise GeminiError(503, "Gemini is not available: could not set up the client.") from exc


def generate_text(prompt: str) -> str:
    client = get_client()
    try:
        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite"),
            contents=prompt,
            config=types.GenerateContentConfig(max_output_tokens=MAX_OUTPUT_TOKENS),
        )
        text = (response.text or "").strip()
    except DefaultCredentialsError as exc:
        # The SDK loads credentials on the first call, not when the client is created.
        logger.exception("Could not load Application Default Credentials")
        raise GeminiError(503, "Gemini is not available: credentials could not be loaded.") from exc
    except Exception as exc:
        logger.exception("The Gemini call failed")
        raise GeminiError(502, "The Gemini request failed. Please try again later.") from exc
    if not text:
        logger.error("Gemini returned no text: %s", response)
        raise GeminiError(502, "Gemini returned an empty response. Please try again later.")
    return text


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "Hey there! What's up?"}


@app.get("/goodbye")
def goodbye() -> dict[str, str]:
    return {"message": "Catch you later!"}


@app.get("/haiku")
def haiku() -> dict[str, str]:
    return {"haiku": generate_text(HAIKU_PROMPT)}


@app.get("/fortune")
def fortune() -> dict[str, str]:
    return {"fortune": generate_text(FORTUNE_PROMPT)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
