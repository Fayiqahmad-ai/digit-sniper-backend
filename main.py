from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import time

app = FastAPI()

# Allow frontend to call this from browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy signal generator for demonstration
class AnalyzeRequest(BaseModel):
    ticks: int = 100

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Digit Sniper Pro backend is running"}

@app.post("/analyze")
def analyze_signal(req: AnalyzeRequest):
    confidence = random.randint(75, 98)
    signal_type = random.choice(["BUY", "SELL", "NO_SIGNAL"])
    timestamp = int(time.time())

    return {
        "signal": signal_type,
        "confidence": confidence,
        "expires_in": 30,
        "timestamp": timestamp,
    }
