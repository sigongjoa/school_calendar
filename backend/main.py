from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import schools, schedules
from database.connection import init_db
import os
from dotenv import load_dotenv

# Load .env
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

app = FastAPI(title="School Calendar API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(schools.router, prefix="/api/schools", tags=["schools"])
app.include_router(schedules.router, prefix="/api/schedules", tags=["schedules"])

@app.on_event("startup")
async def startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8015, reload=True)
