"""Main FastAPI Application Entrypoint.

Initializes the FastAPI application, sets up CORS middleware, registers API routes,
and provides system health check endpoints.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.chat import router as chat_router
from app.core.config import settings

# Initialize FastAPI application instance
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure Cross-Origin Resource Sharing (CORS) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 routers
app.include_router(chat_router, prefix="/api/v1")


@app.get(
    "/api/v1/health",
    tags=["Health"],
    summary="Health Check",
    description="Check the operational health and readiness of the service.",
)
async def health_check() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "healthy"}