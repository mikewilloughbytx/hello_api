# Plan: Gemini /haiku and /fortune endpoints

## Context
The app has `/hello` and `/goodbye`. We are adding two GET endpoints whose text is written by Gemini through Vertex AI, using the `google-genai` SDK and Application Default Credentials only (no API keys or key files). `/hello` and `/goodbye` must keep working even when Gemini is unavailable or not configured.

## Steps
1. **Branch:** stay on `hello_goodbye_api` (already not `main`).
2. **Prompt log:** append a time-stamped entry to `PROMPTS.md` first. Plan mode blocks writing it earlier.
3. **Save plan:** copy this plan to `plans/02_gemini_endpoints.md`.
4. **Dependency:** `poetry add google-genai`. No other packages.
5. **`main.py`:**
   - Settings from the environment: `GOOGLE_CLOUD_PROJECT` (required), `GOOGLE_CLOUD_LOCATION` (default `global`), `GEMINI_MODEL` (default `gemini-3.1-flash-lite`).
   - Create `genai.Client(vertexai=True, project=..., location=..., http_options=HttpOptions(timeout=30000))` lazily on first use and cache it. The app still starts, and `/hello` and `/goodbye` still work, if the project is unset.
   - Fixed prompts as module constants. Neither endpoint takes input.
   - One shared helper calls `generate_content` with `GenerateContentConfig(max_output_tokens=100)` and returns stripped text. Both routes use it. Routes stay sync `def`, so FastAPI runs the blocking call in its threadpool.
   - `GET /haiku` returns `{"haiku": "..."}`; `GET /fortune` returns `{"fortune": "..."}`.
6. **Error handling** (JSON body `{"error": "..."}`):
   - `503` if `GOOGLE_CLOUD_PROJECT` is unset or credentials can't be loaded when the client is created.
   - `502` if the Gemini call fails, or returns empty text (for example, a safety block).
   - Full exception details go to the server log only, so internals don't reach callers.
7. **`requirements.txt`:** re-export with the same `poetry export` command as before.
8. **`README.md`:** add the new endpoints, env vars, error responses, and Vertex AI setup (`aiplatform.googleapis.com` enabled, `gcloud auth application-default login` locally, `roles/aiplatform.user` on Cloud Run's service account).

Commits, pushes and PRs are left to you, per `CLAUDE.md`.

## Files changed
`main.py`, `pyproject.toml`, `poetry.lock`, `requirements.txt`, `README.md`, `PROMPTS.md`, plus new `plans/02_gemini_endpoints.md`

## Verification
- With `GOOGLE_CLOUD_PROJECT` unset: `/haiku` and `/fortune` return 503 JSON; `/hello` and `/goodbye` still return 200.
- With the project set but no credentials: returns JSON 503 or 502 and the server does not crash.
- Live call: this machine has no Application Default Credentials yet, so you need to run `gcloud auth application-default login` (it opens a browser). Then, with `GOOGLE_CLOUD_PROJECT=hello-and-goodbye-api-mcw`, confirm both endpoints return 200 with complete text.
- During the live call, check that the 100-token cap doesn't cut off responses. If thinking tokens use up the budget (`finish_reason` is `MAX_TOKENS`), set the lowest thinking level the model supports.
- Confirm `requirements.txt` lists `google-genai` and that no keys or secrets are in the repo.
