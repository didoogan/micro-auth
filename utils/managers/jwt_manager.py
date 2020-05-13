import jwt

from users.schemas import User

class JwtManager:

    def create_jwt(self, user: User) -> str:
        return jwt.encode(user.dict(), 'secret', algorithm='HS256').decode('ascii')
    
    def decode(self, token: str):
        return jwt.decode(token, 'secret', algorithms=['HS256'])