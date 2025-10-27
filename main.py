from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from db.base import init_db
from models.secret_key import SecretKeyIndex
from models.alerts import BaseAlert
from routes import alert_router
from routes.data.router import data_router
from routes.keys.router import keys_router
from decouple import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
DB_URL = config('MONGO_DB_CONNECTION_STRING')
DB_NAME = config('MONGO_DB_NAME')
ENVIRONMENT = config('ENVIRONMENT', default='development')
ALLOWED_ORIGINS = config('ALLOWED_ORIGINS', default='http://localhost:3000').split(',')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting application in {ENVIRONMENT} mode")
    logger.info(f"Connecting to database: {DB_NAME}")

    try:
        app.state.client = await init_db(
            DB_URL,
            DB_NAME,
            models=[BaseAlert, SecretKeyIndex]
        )
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down application")
    if hasattr(app.state, 'client'):
        app.state.client.close()
        logger.info("Database connection closed")


app = FastAPI(
    title="Arrow Backend API",
    description="Trading alert management system with strategy key authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
# In production, set ALLOWED_ORIGINS to specific domains only
if ENVIRONMENT == 'production':
    logger.warning("Running in production mode with restricted CORS")
    allow_origins = ALLOWED_ORIGINS
else:
    logger.info("Running in development mode with permissive CORS")
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(alert_router)
app.include_router(data_router)
app.include_router(keys_router)


@app.get(
    '/',
    tags=["health"],
    summary="Root endpoint",
    description="Simple endpoint to verify the API is running"
)
async def root():
    """Root endpoint."""
    return {
        "message": "Arrow Backend API is running",
        "version": "1.0.0",
        "environment": ENVIRONMENT
    }


@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Comprehensive health check endpoint for monitoring"
)
async def health():
    """Health check endpoint with database connectivity status."""
    try:
        # Test database connectivity
        await BaseAlert.find_one()
        db_status = "connected"
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        db_status = "disconnected"
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": db_status,
                "error": str(e)
            }
        )

    return {
        "status": "healthy",
        "database": db_status,
        "environment": ENVIRONMENT
    }
