import os

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello() -> dict[str, str]:
    return {"message": "Hey there! What's up?"}


@app.get("/goodbye")
def goodbye() -> dict[str, str]:
    return {"message": "Catch you later!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
