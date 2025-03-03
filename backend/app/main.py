from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from api.routers.admin_router import router as admin_router
from api.routers.students_router import router as student_router
from api.routers.teachers_router import router as teacher_router
from infrastructure.auth import get_permission
from api.routers import auth_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router, prefix="/api", dependencies= [Depends(get_permission("Admin"))])
app.include_router(teacher_router, prefix="/api", dependencies= [Depends(get_permission("Teacher"))])
app.include_router(student_router, prefix="/api", dependencies= [Depends(get_permission("Student"))])
app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])

