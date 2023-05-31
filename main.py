# Import necessary modules and functions
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Create a FastAPI instance
app = FastAPI()

# Define a function to get a database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define a route to get all holidays
@app.get("/holidays/", response_model=list[schemas.Holiday])
def get_all_holiday(db: Session = Depends(get_db)):
    holidays = crud.get_holidays(db=db)
    return holidays

# Define a route to check if a date is a holiday
@app.get("/check/holiday/date/{date}", response_model=schemas.HolidayCheck)
def check_date_is_holiday(date: str, db: Session = Depends(get_db)):
    msg = crud.check_holiday(db=db, query_date=date)
    return msg

# Define a route to get a holiday by its description
@app.get("/holiday/desc/{desc}", response_model=Optional[schemas.Holiday])
def get_holiday_by_desc(desc: str, db: Session = Depends(get_db)):
    msg = crud.get_holiday_by_desc(db=db, query_desc=desc)
    return msg

# Define a route to delete a holiday by its ID
@app.delete("/holiday/{id}")
async def delete_holiday(id: str, db: Session = Depends(get_db)):
    msg = crud.delete_holiday(db=db, id=id)
    return msg

# Define a route to create a new holiday
@app.post("/holiday/", response_model=schemas.HolidayResponse)
def create_holiday(holiday: schemas.Holiday, db: Session = Depends(get_db)):
    return crud.create_holiday(db=db, holiday=holiday)

# Define a route to bulk insert holidays
@app.post("/holidays/")
def create_holidays(holidays: schemas.HolidayList, db: Session = Depends(get_db)):
    crud.create_holidays(db=db, holidays=holidays)
    return {'message': 'successfully bulk inserted'}