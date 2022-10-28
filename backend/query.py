from db import engine
from models.models import *
from sqlmodel import Session, select, or_
from main import StudentData

def select_no_category_table(table):
    with Session(engine) as session:
        statement = select(table)
        result = session.exec(statement)
        first = result.all()
        print(first)
        if not first:
            return []
        return [(row.keyword, row.link) for row in first]

def select_category_table(table, category):
    with Session(engine) as session:
        statement = select(table).where(table.category == category)
        result = session.exec(statement)
        first = result.all()
        if not first:
            return []
        return [(row.keyword, row.link) for row in first]
    
def register_student(student_data: StudentData, table=Student):
    with Session(engine) as session:
        session.add(table(name=student_data.name, 
                          user_name=student_data.user_name,
                          mem_word=student_data.mem_word))