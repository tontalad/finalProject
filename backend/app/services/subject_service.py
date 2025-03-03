from repositories.subject_repo import SubjectRepository
from models.query_params import QueryParams

class SubjectService:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    async def get_by_id(self, subject_id: str):
        return await self.subject_repo.get_by_id(subject_id)
    
    async def get_all(self, query_params: QueryParams):
        return await self.subject_repo.get_all(query_params)
    
    async def create(self, subject):
        return await self.subject_repo.create(subject)
    
    async def update(self, subject_id, subject):
        return await self.subject_repo.update(subject_id, subject)
    
    async def insert_user(self, subject_id, user_data):
        return await self.subject_repo.insert_user_to_subject(subject_id, user_data)
    
    async def insert_multiple_user(self, subject_id, file):
        return await self.subject_repo.insert_multiple_user_to_subject(subject_id, file)