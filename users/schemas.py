from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    password: str


class User(UserIn):
    id: str


class AuthUser(BaseModel):
    id: str
    email: str


class AuthResponse(BaseModel):
    user: AuthUser
    token: str
