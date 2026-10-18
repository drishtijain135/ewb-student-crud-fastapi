
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.database import init_db
from app.schemas import StudentCreate
from app.crud import create_student, get_all_students

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="EWB Student Database API",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {"message": "Student Database API is running"}


@app.post("/students")
def add_student(student: StudentCreate):
    try:
        student_data = student.model_dump(mode="json")
        return create_student(student_data)
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

@app.get("/students")
def list_students():
    return get_all_students()
