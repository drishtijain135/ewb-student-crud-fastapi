
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.database import init_db
from app.schemas import StudentCreate, AIQuestion
from app.crud import(
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,

)
from app.ai_services import ask_ollama
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

@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = get_student_by_id(student_id)
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student


@app.put("/students/{student_id}")
def edit_student(student_id: int, student: StudentCreate):
    try:
        student_data = student.model_dump(mode="json")
        updated_student = update_student(student_id, student_data)

        if updated_student is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return updated_student

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@app.delete("/students/{student_id}")
def remove_student(student_id: int):
    deleted = delete_student(student_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"message": "Student deleted successfully"}

@app.post("/ask")
def ask_question(request: AIQuestion):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    students = get_all_students()

    try:
        answer = ask_ollama(question, students)
        return {
            "question": question,
            "answer": answer
        }

    except RuntimeError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

