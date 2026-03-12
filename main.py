from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests

app = FastAPI()

# allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve the chatbot UI
@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/chat")
def chat(q: str):

    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": q + ". Answer in 2 short lines.",
                "stream": False
            },
            timeout=60
        )

        data = r.json()

        return {"response": data["response"]}

    except Exception:
        return {
            "response": "AI model is not connected on the server yet. This is a demo deployment."
        }
