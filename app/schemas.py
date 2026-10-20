
from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None


class StudentResponse(BaseModel):
    id: int
    name: str
    date_of_birth: date
    email: Optional[str] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None
    created_at: Optional[str] = None


class AIQuestion(BaseModel):
    question: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="A natural-language question about student records",
    )

