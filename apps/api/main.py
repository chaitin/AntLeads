"""FastAPI application for AntLeads."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from apps.api.config import settings
from apps.api.database import init_db
from apps.api.routes import automation, funnel, leads, tasks, widgets


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="AntLeads API",
    description="AI-driven lead management and marketing automation system",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(funnel.router, prefix="/api/v1/funnel", tags=["funnel"])
app.include_router(automation.router, prefix="/api/v1/automation", tags=["automation"])
app.include_router(widgets.router, prefix="/api/v1/widgets", tags=["widgets"])

# Serve widget static files
app.mount("/static", StaticFiles(directory="apps/widget/src"), name="static")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AntLeads API",
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
