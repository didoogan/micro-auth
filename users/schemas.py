from pydantic import BaseModel, EmailStr, constr


class UserIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=40)


class User(UserIn):
    id: str


class AuthUser(BaseModel):
    id: str
    email: EmailStr


class AuthResponse(BaseModel):
    user: AuthUser
    token: str
