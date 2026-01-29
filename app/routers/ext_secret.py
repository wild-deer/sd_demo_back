from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import secrets

router = APIRouter(prefix="/knowledgeService", tags=["mock"])


class GenerateAppKeyRequest(BaseModel):
    appId: str
    appSecret: str


@router.post("/extSecret/generateAppKey")
async def generate_app_key():
    app_key = f"{secrets.token_hex(32)}.{int(datetime.now().timestamp() * 1000)}"
    return {
        "data": None,
        "isUpdate": None,
        "model": None,
        "requestId": None,
        "resultCode": "0",
        "resultMsg": "",
        "resultObject": {"appKey": app_key},
    }

