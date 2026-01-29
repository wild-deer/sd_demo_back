import json
from fastapi import APIRouter, Body, Depends, File, HTTPException, UploadFile, status, Form
from datetime import timedelta


from models import User, Token, Message
from core import security

router = APIRouter(prefix="/users", tags=["用户接口"])

# 模拟用户库
fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "hashed_password": "fakehashedpassword123",
    }
}

def fake_verify_password(plain_password, hashed_password):
    # 模拟密码验证
    return plain_password == "secret" and hashed_password == "fakehashedpassword123"

@router.post("/login", response_model=Token, summary="用户登录", description="用户登录接口，返回JWT token")
async def login(username: dict = Form(...), password: str = Form(...)):

    user_dict = fake_users_db.get(username.username)
    if not user_dict or not fake_verify_password(password, user_dict["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user_dict["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User, summary="获取当前用户信息", description="获取当前登录用户的信息")
async def read_users_me(current_user=Depends(security.get_current_user)):
    # current_user 是JWT中的payload，可以根据需要扩展
    return {"id": 1, "username": current_user["sub"]}






@router.post("/test", summary="测试接口", description="测试接口",response_model=Message)

async def test(data: str =Form('默认消息')):
    print(data)
    return {"message": "测试成功"}

