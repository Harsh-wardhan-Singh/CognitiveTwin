from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pathlib import Path
import traceback

from app.db.session import engine
from app.db.base import Base

from app.models.user import User
from app.models.classroom import Classroom
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.mastery import Mastery
from app.models.classroom_student import ClassroomStudent

from app.core.dependencies import get_current_user
from app.core.logging import get_logger
from app.core.exceptions import CognitiveException
from app.api.auth_routes import router as auth_router
from app.api.teacher_routes import router as teacher_router
from app.api.student_routes import router as student_router
from app.api.quiz_routes import router as quiz_router

# Initialize logger
logger = get_logger("main")

app = FastAPI(
    title="Cognitive Twin Backend",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(teacher_router)
app.include_router(student_router)
app.include_router(quiz_router)

# Create tables
Base.metadata.create_all(bind=engine)

# ============================================
# ERROR HANDLING MIDDLEWARE
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with better messages"""
    errors = exc.errors()
    details = []
    for error in errors:
        field = ".".join(str(x) for x in error["loc"][1:])
        details.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.error(f"Validation error: {details}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": details
        }
    )

@app.exception_handler(CognitiveException)
async def cognitive_exception_handler(request: Request, exc: CognitiveException):
    """Handle custom cognitive exceptions"""
    logger.error(f"{exc.error_code}: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "path": str(request.url.path)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )

# ============================================
# HEALTH CHECKS & UTILITY ENDPOINTS
# ============================================

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cognitive_twin"}


@app.get("/protected")
def protected(user=Depends(get_current_user)):
    """Protected endpoint - requires authentication"""
    return {"user": user}


# ============================================
# STARTUP & SHUTDOWN
# ============================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("🚀 Cognitive Twin Backend starting up...")
    logger.info("✅ Database tables initialized")
    logger.info("✅ Routes registered")
    logger.info("✅ Service container ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("🛑 Cognitive Twin Backend shutting down...")


# ============================================
# STATIC FILE SERVING (Frontend)
# ============================================

# Serve static frontend files
frontend_path = Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    logger.info(f"📁 Static frontend mounted from: {frontend_path}")
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    logger.warning(f"⚠️  Frontend directory not found at {frontend_path}")


