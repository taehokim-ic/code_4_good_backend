from audioop import add
from backend.models.models import EventFeedback
from db import engine
from models.models import *
from sqlmodel import Session, select, or_
from pydantic import BaseModel
from datetime import date

class StudentData(BaseModel):
    user_name: str
    name: str = None
    mem_word: str
    
    class Config:
        orm_mode = True
        
class EventData(BaseModel):
    name: str
    date: datetime

    class Config:
        orm_mode = True
        
class EventFeedbackData(BaseModel):
    event: EventData
    user_name:str
    mem_word: str
    feedback_star: int
    feedback_message: str

# Adds student to student database, returns False if student exists    
def registered_student(student_data: StudentData, table=Student):
    student_exists = check_if_student_exists(student_data=student_data) 
    with Session(engine) as session:    
        if not student_exists:
            session.add(table(name=student_data.name, 
                          user_name=student_data.user_name,
                          mem_word=student_data.mem_word))
            session.commit()
            return True
        else:
            session.commit()
            return False
        
# Checks if student exists in student database
def check_if_student_exists(student_data: StudentData, table=Student):
    with Session(engine) as session:
        statement = select(table).where(table.user_name==student_data.user_name,
                                        table.mem_word==student_data.mem_word)
        result = session.exec(statement=statement).all()
        
        # No student found
        if len(result) == 0:
            return False

        return True
        
# Getting events on or after a certain date
def get_event_on_or_after_specific_date(date: datetime, table=Events):
    with Session(engine) as session:
        statement = select(table).where(table.date>=date)
        result = session.exec(statement=statement).all()
        
        return result    
    
# Getting events for a certain date
def get_event_at_specific_date(date: datetime, table=Events):
    with Session(engine) as session:
        statement = select(table).where(table.date==date)
        result = session.exec(statement=statement).all()
        
        return result
    
# Add event for specific date
def add_event_at_specific_date(event_data: EventData, table=Events):
    with Session(engine) as session:
        session.add(table(name=event_data.name, 
                          date=event_data.date))
        session.commit()
        
# Checks if event has been added
def event_added(event_data: EventData, table=Events):
    with Session(engine) as session:
        statement = select(table).where(table.name==event_data.name,
                                        table.date==event_data.date)
        result = session.exec(statement=statement).all()
        
        # No event found
        if len(result) == 0:
            return False

        return True

# Add check_in data, returns True if added
def add_check_in(event_data: EventFeedbackData, table=EventFeedback):
    added_event = event_added(event_data=event_data.event)
    added_student = check_if_student_exists(
        StudentData(user_name=event_data.user_name, 
                    mem_word=event_data.mem_word))
    flag = added_event and added_student
    with Session(engine) as session:
        if flag:
            session.add(table(
                name=event_data.event.name,
                date=event_data.event.date,
                user_name=event_data.user_name,
                feedback_star=event_data.feedback_star,
                feedback_message=event_data.feedback_message
            ))
        session.commit()

    return flag         
        
if __name__ == "__main__":
    new_student = EventData(name="TD22Dho", date=datetime.today())
    add_event_at_specific_date(new_student)
    print(get_event_on_or_after_specific_date(datetime.today()))