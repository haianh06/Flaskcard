from fastapi import FastAPI
from .routers.deck import router as deck_router
from .routers.word import router as word_router
from .routers.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI(title  = "Flashcard", description = "A flashcard app for learning Japanese")
app.include_router(deck_router)
app.include_router(word_router)
app.include_router(auth_router)

# Read allowed origins from env, defaulting to localhost for dev
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:8080,http://localhost:5173,http://localhost:3000")
origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]

# Include FRONTEND_URL if explicitly set
frontend_url = os.getenv("FRONTEND_URL")
if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import subprocess

@app.get("/seed_database")
async def seed_database():
    """Temporary endpoint to seed the database on Render"""
    # Run migrations and then the seeding script as a background process so the request doesn't timeout
    # Use powershell if on Windows, or sh on Linux (Render uses Linux)
    subprocess.Popen("alembic upgrade head && python seed_all_words.py", shell=True)
    return {"message": "Database migrations and seeding have been started in the background! It will take about 2-3 minutes. Please check your Render logs."}