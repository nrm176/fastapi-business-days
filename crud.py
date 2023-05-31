import logging
import traceback

from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas


def create_holiday(db: Session, holiday: schemas.Holiday):
    holiday = models.Holiday(**holiday.dict())
    db.add(holiday)
    db.commit()
    db.refresh(holiday)
    return holiday


def create_holidays(db: Session, holidays: schemas.HolidayList):
    try:
        records = [models.Holiday(**holiday.dict()) for holiday in holidays.data]
        db.bulk_save_objects(records)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete item")
    finally:
        db.close()
    # for record in records:
    #     db.refresh(record)
    # # # return records
    # # db.refresh(records)
    # return records


def get_holidays(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Holiday).offset(skip).limit(limit).all()


def check_holiday(db: Session, query_date: str):
    record = db.query(models.Holiday).filter_by(date=query_date).first()
    if not record:
        return {"is_holiday": False, "holiday": None}
    return {"is_holiday": True, "holiday": record}


def get_holiday_by_desc(db: Session, query_desc: str):
    record = db.query(models.Holiday).filter_by(desc=query_desc).first()
    return record


def delete_holiday(db: Session, id: str):
    try:
        record = db.query(models.Holiday).filter_by(id=id).first()
        logging.info(record)
        if not record:
            raise HTTPException(status_code=404, detail="record not found")
        db.delete(record)
        db.commit()
        return {'message': 'record has been deleted'}
    except:
        db.rollback()
        logging.ERROR(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to delete item")
    finally:
        db.close()
