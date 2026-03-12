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

    try:

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": q}
                    ]
                }
            ]
        }

        r = requests.post(url, json=payload)

        data = r.json()

        print(data)

        if "candidates" in data:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            answer = "AI couldn't generate a response."

        return {"response": answer}

    except Exception as e:
        print(e)
        return {"response": "Server error. Please try again."}
