from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """Health check endpoint for monitoring and frontend connectivity tests."""
    return {"status": "healthy"}
