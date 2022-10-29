from fastapi import FastAPI
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

# Invalid Endpoint
@app.get('/')
def default():
    return {"message": "invalid API endpoint"}

# Student Register
@app.post('/ignitehub/api/v1/register')
def register_student(student_data: StudentData = None):
    
    registered = registered_student(student_data=student_data)
    
    if registered:
        return {"message": "Success"} 
    else:
        return {"message": "Fail"}

# Check Out
@app.post('/ignitehub/api/v1/check_in')
def check_in(event: EventFeedbackData):
    check_in_added = add_check_in(event_data=event)
    
    if check_in_added:
        return {"message": "Check-in Successful."}
    else:
        return {"message": "Invalid Data, Check Values Again."}
   
# Check Out
@app.post('/ignitehub/api/v1/check_out')
def check_out(event: EventFeedbackData):
    check_out_added = add_check_out(event_data=event)
    
    if check_out_added:
        return {"message": "Check-out Successful."}
    else:
        return {"message": "Invalid Data, Check Values Again."}
        
# Add Event
@app.post('/ignitehub/api/v1/add_event')
def add_event(event: EventData):
    
    add_event_at_specific_date(event_data=event)
    
    return {"message": "Event Added!"}

    # Error Handling Required in the Future

# Get Future Events
@app.get('/ignitehub/api/v1/events')
def events_get():
    events = get_event_on_or_after_specific_date(datetime.today())

    return {"events": [event for event in events]}

# Get All Events
@app.get('/ignitehub/api/v1/all_events')
def events_get():
    events = get_all_events()

    return {"events": [event for event in events]}    
    
# Events Available Today
@app.get('/ignitehub/api/v1/event_today')
def get_event_today():
    events = get_event_at_specific_date(datetime.today())
    
    return {"events": [event for event in events]}
    
# Get Feedback
@app.get('/ignitehub/api/v1/feedback')
def feedback_get():

    return {"message": "NEEDS WORK"}