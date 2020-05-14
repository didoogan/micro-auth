from users.models import users

import utils
from database import database
from users.schemas import UserIn


class UserManager:

    model = users

    @property
    def query_manager(self):
        return utils.QueryManager(users)

    @property
    def password_manager(self):
        return utils.PasswordManager()

    async def get_by_email(self, email):
        query = self.query_manager.filter({'email': email})
        return await database.fetch_one(query)

    async def create(self, user: UserIn):
        user.password = self.password_manager.hash_password(
            user.password
        )
        query = self.query_manager.create(user.dict())
        return await database.execute(query)



