from datetime import date
from typing import Optional
from sqlalchemy import table

from sqlmodel import SQLModel, Field

class Student(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
    user_name: str
    mem_word: str

class Events(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
    date: date
    
class Volunteer(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True)
    date: date
    
class EventFeedback(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    date: date
    user_name: str
    feedback_star: int
    feedbacK_msg: str