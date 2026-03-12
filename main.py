from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "https://college-ai-chatbot-theta.vercel.app"
    ],
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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": q}]
                }
            ]
        }

        r = requests.post(url, json=payload, timeout=30)

        data = r.json()

        # Gemini sometimes returns different structures
        if "candidates" in data and len(data["candidates"]) > 0:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]

        elif "error" in data:
            answer = "AI service error. Please try again later."

        elif "promptFeedback" in data:
            answer = "The question was blocked by the AI safety filter."

        else:
            answer = "AI couldn't generate a response. Please try again."

        return {"response": answer}

    except Exception as e:
        return {"response": "AI server starting. Please try again in a moment."}
