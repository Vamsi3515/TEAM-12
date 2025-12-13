from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import github, ats, security

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
app.include_router(security.router)
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the Mirai API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}
