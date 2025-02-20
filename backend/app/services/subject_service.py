from repositories.subject_repo import SubjectRepository

class SubjectService:
    def __init__(self, subject_repo: SubjectRepository):
        self.subject_repo = subject_repo

    async def get_by_id(self, subject_id: str):
        return await self.subject_repo.get_by_id(subject_id)
    
    async def get_all(self):
        return await self.subject_repo.get_all()
    
    async def create(self, subject):
        return await self.subject_repo.create(subject)
    
    async def update(self, subject_id, subject):
        return await self.subject_repo.update(subject_id, subject)
    
       