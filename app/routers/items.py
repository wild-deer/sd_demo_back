from fastapi import APIRouter, Depends
from core.security import get_current_user

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def read_items(current_user=Depends(get_current_user)):
    return [{"item_id": "foo", "owner": current_user["sub"]}]