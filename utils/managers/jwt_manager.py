import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError

from users.schemas import User
from fastapi import HTTPException


class JwtManager:

    def create_jwt(self, user: User) -> str:
        try:
            return jwt.encode(
                user.dict(),
                'secret',
                algorithm='HS256',
            ).decode('ascii')
        except InvalidSignatureError:
            raise HTTPException(status_code=422, detail='JWT processing error')

    def decode(self, token: str):
        try:
            return jwt.decode(token, 'secret', algorithms=['HS256'])
        except DecodeError:
            raise HTTPException(status_code=422, detail='JWT processing error')
