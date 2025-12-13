from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import github
from app.routers import ats
from app.routers import authenticity
from app.routers import security
from app.routers import uml
from app.routers import learning

app = FastAPI(
    title="Mirai Hackathon API",
    description="FastAPI backend for hackathon project",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github.router, prefix="/api")
app.include_router(ats.router, prefix="/api")
app.include_router(authenticity.router, prefix="/api")
app.include_router(security.router, prefix="/api")
app.include_router(uml.router, prefix="/api")
app.include_router(learning.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the Mirai API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}
