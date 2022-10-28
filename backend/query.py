from db import engine
from models.models import *
from sqlmodel import Session, select, or_
from pydantic import BaseModel


class StudentData(BaseModel):
    user_name: str
    name: str
    mem_word: str
    
    class Config:
        orm_mode = True

# def select_no_category_table(table):
#     with Session(engine) as session:
#         statement = select(table)
#         result = session.exec(statement)
#         first = result.all()
#         print(first)
#         if not first:
#             return []
#         return [(row.keyword, row.link) for row in first]

# def select_category_table(table, category):
#     with Session(engine) as session:
#         statement = select(table).where(table.category == category)
#         result = session.exec(statement)
#         first = result.all()
#         if not first:
#             return []
#         return [(row.keyword, row.link) for row in first]

# Adds student to stuednt database, returns False if student exists    
def register_student(student_data: StudentData, table=Student):
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
        
if __name__ == "__main__":
    new_student = StudentData(name="TD22Dho", user_name="23dwd22123U", mem_word="Taego")
    register_student(new_student)
    