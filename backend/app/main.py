from app.routers import entities, entity_types, health
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="EAV CMS API",
    description="Backend API for the EAV CMS application",
    version="0.1.0",
)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(entity_types.router)
app.include_router(entities.router)


@app.get("/")
async def root():
    return {"message": "EAV CMS API", "docs": "/docs"}
