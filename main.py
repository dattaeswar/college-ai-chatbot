from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return FileResponse("index.html")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/chat")
def chat(q: str):

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [
            {
                "parts": [{"text": q}]
            }
        ]
    }

    r = requests.post(url, json=payload)

    data = r.json()

    answer = data["candidates"][0]["content"]["parts"][0]["text"]

    return {"response": answer}
