from models.user import User, UserResponse, UserListResponseFromSubject
from repositories.user_repo import UserRepository

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_user_by_subject(self, subject_id: str) -> UserListResponseFromSubject:
        return await self.repo.get_users_by_subject_id(subject_id)

    async def get_user(self, user_id: str) -> UserResponse | None:
        return await self.repo.get_by_id(user_id)

    async def create_user(self, user: User) -> UserResponse:
        return await self.repo.create(user)
    
    async def get_user_by_email(self, email: str) -> UserResponse | None:
        return await self.repo.get_by_email(email)
