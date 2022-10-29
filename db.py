from sqlmodel import create_engine, SQLModel
from models.models import *

db_file_name = "database3.db"
DATABASE_URL = f"sqlite:///{db_file_name}"

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()