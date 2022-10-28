from fastapi import FastAPI
import uvicorn
from query import *

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI()

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

@app.post('/ignitehub/api/v1/register')
def process_message(student_data: StudentData = None):
    
    registered = register_student(student_data=student_data)
    
    if registered:
        return {"message": "Success"} 
    else:
        return {"message": "Fail"}
    
if __name__ == "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8000)