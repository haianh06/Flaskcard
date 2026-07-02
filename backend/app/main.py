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
    return {"message": "Database migrations and seeding have been started in the background! Please check /seed_progress to see the progress."}

from sqlalchemy import text
from .database import SessionDep

@app.get("/seed_progress")
async def seed_progress(session: SessionDep):
    """Temporary endpoint to check the progress of the database seeding"""
    try:
        # Get the total number of words in the database
        result = await session.execute(text("SELECT count(*) FROM word"))
        count = result.scalar()
        total = 217674
        percentage = round((count / total) * 100, 2) if count else 0
        return {
            "status": "Seeding in progress" if count < total else "Completed",
            "current_count": count,
            "total_words": total,
            "progress_percent": percentage
        }
    except Exception as e:
        # If table doesn't exist yet, return 0
        return {
            "status": "Initializing (Creating tables or downloading data...)",
            "current_count": 0,
            "total_words": 217674,
            "progress_percent": 0.0
        }