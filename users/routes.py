from typing import List

from fastapi import APIRouter, HTTPException, Header
from fastapi_utils.cbv import cbv

import utils
from .models import users
from .schemas import User, UserIn, AuthResponse, AuthUser
from database import database


router = APIRouter()

@router.get('/', response_model=List[User])
async def read_users():
    query = users.select()
    result = await database.fetch_all(query)
    return result


@router.post('/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(email=user.email, password=user.password)
    last_user_id = await database.execute(query)
    return {**user.dict(), 'id': last_user_id}


@cbv(router)
class UserRoutes:

    query_manager = utils.QueryManager(users)
    jwt_manager = utils.JwtManager()
    user_manager = utils.UserManager()
    password_manager = utils.PasswordManager()

    @router.post('/signup', response_model= AuthResponse)
    async def sign_up(self, user: UserIn):
        existed_user = await self.user_manager.get_by_email(user.email)
        if existed_user:
            raise HTTPException(status_code=400, detail='User already exists')
        last_user_id = await self.user_manager.create(user) 
        user_with_id = {**user.dict(), 'id': last_user_id}
        response_user = AuthUser(**user_with_id)
        token = self.jwt_manager.create_jwt(response_user)
        return {'user': response_user, 'token': token}
    

    @router.post('/signin', response_model=AuthResponse)
    async def sign_in(self, user: UserIn):
        existed_user = await self.user_manager.get_by_email(user.email)
        if not existed_user:
            raise HTTPException(status_code=400, detail='Wrong credentials')
        verified_password = self.password_manager.verify_password(
            existed_user.password, user.password
        )
        if not verified_password:
            raise HTTPException(status_code=400, detail='Wrong credentials')
        response_user = AuthUser(**existed_user)
        return {'user': response_user,
            'token': self.jwt_manager.create_jwt(response_user)
        }

    @router.get('/user-info', response_model=AuthUser)
    def user_info(self, *, authentication: str = Header(None)):
        return self.jwt_manager.decode(authentication)