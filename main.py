from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import requests
import os

app = FastAPI()

# CORS configuration (allow frontend domains)
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

# Serve homepage
@app.get("/")
def home():
    return FileResponse("index.html")

# Read Gemini API key from environment variable
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

        answer = data["candidates"][0]["content"]["parts"][0]["text"]

        return {"response": answer}

    except Exception as e:
        return {
            "response": "Sorry, the AI server is starting. Please try again in a moment."
        }
