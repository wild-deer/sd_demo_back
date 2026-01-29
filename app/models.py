from fastapi import Form
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


from pydantic import BaseModel



class Message(BaseModel, extra='forbid'):
    message: str = Form('默认消息')
