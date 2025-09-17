from __future__ import annotations
from sqlmodel import SQLModel, Field
from pydantic import validator
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, max_length=50)
    password: str = Field(max_length=256)

    external_id: Optional[str] = Field(default=None, max_length=30)
    student_id: Optional[str] = Field(default=None, max_length=20)
    full_name: Optional[str] = Field(default=None, max_length=150)

    gender: Optional[str] = Field(default=None, max_length=10, description="Male / Female")
    faculty_id: Optional[int] = Field(default=None, description="Fakultetning ID raqami")
    turniket_id: Optional[str] = Field(default=None, max_length=20)

    group_id: Optional[int] = Field(default=None)
    group_name: Optional[str] = Field(default=None, max_length=100)

    speciality_id: Optional[str] = Field(default=None, max_length=20)
    speciality_name: Optional[str] = Field(default=None, max_length=150)

    begin_time: Optional[datetime] = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    image_url: Optional[str] = Field(default=None, max_length=500)
    file_path: Optional[str] = Field(default=None, max_length=500)

    def to_dict(self) -> dict:
        return self.dict()

    @validator("gender")
    def validate_gender(cls, v):
        if v and v.lower() not in ("male", "female"):
            raise ValueError("Gender must be 'Male' or 'Female'")
        return v.title() if v else None

    @validator("student_id")
    def validate_student_id(cls, v):
        if v and not v.isdigit():
            raise ValueError("Student ID must be numeric")
        return v

    @validator("begin_time", "end_time", "created_at", pre=True, always=True)
    def validate_datetime(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v)
        return v

class Filologiya(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(index=True, max_length=50)
    password: str = Field(max_length=256)

    external_id: Optional[str] = Field(default=None, max_length=30)
    student_id: Optional[str] = Field(default=None, max_length=20)
    full_name: Optional[str] = Field(default=None, max_length=150)

    gender: Optional[str] = Field(default=None, max_length=10, description="Male / Female")
    faculty_id: Optional[int] = Field(default=None, description="Fakultetning ID raqami")
    turniket_id: Optional[str] = Field(default=None, max_length=20)

    group_id: Optional[int] = Field(default=None)
    group_name: Optional[str] = Field(default=None, max_length=100)

    speciality_id: Optional[str] = Field(default=None, max_length=20)
    speciality_name: Optional[str] = Field(default=None, max_length=150)

    begin_time: Optional[datetime] = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    image_url: Optional[str] = Field(default=None, max_length=500)
    file_path: Optional[str] = Field(default=None, max_length=500)

    def to_dict(self) -> dict:
        return self.dict()

    @validator("gender")
    def validate_gender(cls, v):
        if v and v.lower() not in ("male", "female"):
            raise ValueError("Gender must be 'Male' or 'Female'")
        return v.title() if v else None

    @validator("student_id")
    def validate_student_id(cls, v):
        if v and not v.isdigit():
            raise ValueError("Student ID must be numeric")
        return v