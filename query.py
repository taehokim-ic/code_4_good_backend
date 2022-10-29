from db import engine
from models.models import *
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import date, datetime, timedelta

class StudentData(BaseModel):
    user_name: str
    name: str = None
    mem_word: str
    
    class Config:
        orm_mode = True
        
class EventData(BaseModel):
    name: str
    date: date 

    class Config:
        orm_mode = True

class EventName(BaseModel):
    name: str
    
    class Config:
        orm_mode = True

class CheckInData(BaseModel):
    name: str
    date: date
    student_name: str
    user_name: str 
    mem_word: str       

class EventFeedbackData(BaseModel):
    name: str
    date: date
    user_name:str
    mem_word: str
    feedback_star: str
    feedback_message: str
    
    class Config:
        orm_mode = True

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
        
# Checks if student exists in database, Student database by default
def check_if_student_exists(student_data: StudentData, table=Student):
    with Session(engine) as session:
        statement = select(table).where(table.user_name==student_data.user_name,
                                        table.name==student_data.name,
                                        table.mem_word==student_data.mem_word)
        result = session.exec(statement=statement).all()
        
        # No student found
        if len(result) == 0:
            return False

        return True

# Checks if student exists in check_in
def check_if_student_exists_check_in(student_data: StudentData, table=CheckIn):
    with Session(engine) as session:
        statement = select(table).where(table.user_name==student_data.user_name)
        result = session.exec(statement=statement).all()
        
        # No student found
        if len(result) == 0:
            return False

        return True
        
# Getting events on or after a certain date
def get_event_on_or_after_specific_date(date: date, table=Events):
    with Session(engine) as session:
        statement = select(table).where(table.date>=date)
        result = session.exec(statement=statement).all()
        
        return result    
    
# Getting events for a certain date
def get_event_at_specific_date(date: date, table=Events):
    with Session(engine) as session:
        statement = select(table).where(table.date==date)
        result = session.exec(statement=statement).all()
        
        return result
    
# Getting events for a certain date
def get_all_events(table=Events):
    with Session(engine) as session:
        statement = select(table.name).distinct()
        result = session.exec(statement=statement).all()
        
        return result

def get_feedback_for_specific_event(name: str, table=EventFeedback):
    with Session(engine) as session:
        statement = select(table).where(table.name==name)
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

# Add check_out data, returns True if added
def add_check_out(event_data: EventFeedbackData, table=EventFeedback, 
                  verify_table=CheckIn):
    added_event = event_added(EventData(name=event_data.name,
                                        date=event_data.date), table=verify_table)
    added_student = check_if_student_exists_check_in(
        StudentData(user_name=event_data.user_name, 
                    mem_word=event_data.mem_word), table=verify_table)
    print(added_event, added_student)
    flag = added_event and added_student
    with Session(engine) as session:
        if flag:
            statement = select(table).where(table.name==event_data.name,
                                        table.date==event_data.date,
                                        table.user_name==event_data.user_name)
            result = session.exec(statement=statement).all()
        
            # Duplication found
            if len(result) != 0:
                flag = False
            
            else:
                session.add(table(
                    name=event_data.name,
                    date=event_data.date,
                    user_name=event_data.user_name,
                    feedback_star=int(event_data.feedback_star),
                    feedback_msg=event_data.feedback_message))
        
        session.commit()

    return flag         

# Add check_in data, returns True if added
def add_check_in(check_in_data: CheckInData, table=CheckIn):
    flags = [True] * 2
    added_event = event_added(EventData(name=check_in_data.name,
                                        date=check_in_data.date), table=Events)
    added_student = check_if_student_exists(
        StudentData(user_name=check_in_data.user_name,
                    name=check_in_data.student_name, 
                    mem_word=check_in_data.mem_word))
    
    flag = added_event and added_student
    flags[0] = flag
    with Session(engine) as session:
        if flag:
            statement = select(table).where(table.name==check_in_data.name,
                                        table.date==check_in_data.date,
                                        table.student_name==check_in_data.student_name,
                                        table.user_name==check_in_data.user_name)
            result = session.exec(statement=statement).all()
        
            # Duplication found
            if len(result) != 0:
                flag1 = False
                flags[1] = flag1
            else:
                session.add(table(
                    name=check_in_data.name,
                    date=check_in_data.date,
                    student_name=check_in_data.student_name,
                    user_name=check_in_data.user_name
                ))
                session.commit()
    print(flags)
    return flags        

        
if __name__ == "__main__":
    
    # print(get_all_events())
    # object = CheckInData(name="Introduction To Python",
    #             date=datetime(2022, 10, 29).date(),
    #             student_name="Mike Hawk",
    #             user_name="fuzzywuzzy",
    #             mem_word="insomnia")
    # add_check_in(object)
    new_student = StudentData(user_name="fuzzywuzzy", 
                              name="Mike Hawk", 
                              mem_word="insomnia")
    new_student1 = StudentData(user_name="buzzywuzzy", 
                              name="John Doe", 
                              mem_word="overworked")
    new_student2 = StudentData(user_name="guardian_angel_154", 
                              name="Nick Nicklas", 
                              mem_word="anime")
    
    registered_student(new_student)
    registered_student(new_student1)
    registered_student(new_student2)
    
    new_event = EventData(name="Introduction To Python", date=datetime.today())
    new_event1 = EventData(name="Introduction To Python", date=(datetime.today() + timedelta(days=7)))
    new_event2 = EventData(name="Introduction To Python", date=datetime.today() + timedelta(days=14))
    new_event3 = EventData(name="Introduction To Python", date=datetime.today() + timedelta(days=21))
    
    new_event4 = EventData(name="Introduction To Java", date=datetime.today() + timedelta(days=1))
    new_event5 = EventData(name="Introduction To Java", date=datetime.today() + timedelta(days=8))
    new_event6 = EventData(name="Introduction To Java", date=datetime.today() + timedelta(days=15))
    
    new_event7 = EventData(name="Introduction To Haskell", date=datetime.today())
    new_event8 = EventData(name="Introduction To Haskell", date=datetime.today() + timedelta(days=3))
    new_event9 = EventData(name="Introduction To Haskell", date=datetime.today() + timedelta(days=7))
    new_event10 = EventData(name="Introduction To Haskell", date=datetime.today() + timedelta(days=10))    
    
    add_event_at_specific_date(new_event)
    add_event_at_specific_date(new_event1)
    add_event_at_specific_date(new_event2)
    add_event_at_specific_date(new_event3)
    add_event_at_specific_date(new_event4)
    add_event_at_specific_date(new_event5)
    add_event_at_specific_date(new_event6)
    add_event_at_specific_date(new_event7)
    add_event_at_specific_date(new_event8)
    add_event_at_specific_date(new_event9)
    add_event_at_specific_date(new_event10)
    
    # object = EventFeedbackData(
    #     name = "Introduction To Python",
    #     date = "2022-10-29",
    #     user_name = "fuzzywuzzy",
    #     mem_word = "insomnia",
    #     feedback_star= "40",
    #     feedback_message = "terrible"
    # )
    
    # object1 = CheckInData(name="Introduction To Python",
    #             date=datetime(2022, 11, 12).date(),
    #             student_name="John Doe",
    #             user_name="buzzywuzzy",
    #             mem_word="overworked")
    # add_check_in(object1)
    
    # object1 = EventFeedbackData(
    #     name = "Introduction To Python",
    #     date = "2022-11-12",
    #     user_name = "buzzywuzzy",
    #     mem_word = "overworkd",
    #     feedback_star= "69",
    #     feedback_message = "average"
    # )
    # add_check_out(object)
    # add_check_out(object1)
    
    # print(get_all_events())