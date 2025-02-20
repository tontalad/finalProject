from models.user import User
from repositories.user_repo import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user(self, user_id: str) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def create_user(self, user: User) -> str:
        return await self.repo.create(user)
