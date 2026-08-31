# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app.api.v1.chat import router as chat_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}