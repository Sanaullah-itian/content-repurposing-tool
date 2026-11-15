from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from generator import generate_linkedin, generate_twitter, generate_email
from ml_features import analyze_sentiment, word_frequency
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogRequest(BaseModel):
    text: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(request: LoginRequest):
    if request.username == "admin" and request.password == "1234":
        return {"status": "success"}
    return {"status": "error"}

@app.post("/generate")
def generate_content(request: BlogRequest):
    linkedin = generate_linkedin(request.text)
    twitter = generate_twitter(request.text)
    email = generate_email(request.text)
    sentiment, polarity = analyze_sentiment(request.text)
    
    # 🔥 NAYA: Word cloud aur Pie chart ke liye data
    word_freq = word_frequency(request.text, top_n=10)
    
    return {
        "linkedin": linkedin, "twitter": twitter, "email": email,
        "sentiment": sentiment, "polarity": polarity,
        "word_freq": word_freq
    }

@app.post("/batch")
async def batch_process(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    results = []
    for index, row in df.iterrows():
        text = row['text']
        sentiment, _ = analyze_sentiment(text)
        results.append({"text": text[:30] + "...", "sentiment": sentiment})
    
    all_text = " ".join(df['text'].astype(str).tolist())
    freq = word_frequency(all_text, top_n=8)
    
    return {"batch_results": results, "word_freq": freq}

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def serve_login():
    return FileResponse("frontend/index.html")