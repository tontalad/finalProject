from repositories.student_repo import StudentRepository

class StudentService:
    def __init__(self, repo: StudentRepository):
        self.repo = repo
    
    async def get_students(self):
        return await self.repo.get_students()
    
    async def get_student_by_id(self, user_id: str):
        return await self.repo.get_student_by_id(user_id)