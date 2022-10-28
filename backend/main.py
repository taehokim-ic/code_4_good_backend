from fastapi import FastAPI
from pydantic import BaseModel


from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

random_messages = [
    "This is the result you're looking for",
    "Please follow the link for more information"
]

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        # you probably want some kind of logging here
        return Response("Internal server error", status_code=500)
        
app.middleware('http')(catch_exceptions_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StudentData(BaseModel):
    username: str
    name: str
    mem_word: str
    
    
    class Config:
        orm_mode = True

@app.post('/ignitehub/api/v1/register')
def process_message(student_data: StudentData = None):
    
    add_message(message=message)
    
    if not link:
        return {
            "message": "Success"
        }
    return {
        "message": "Fail"
    }