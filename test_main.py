from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app, get_db
from fastapi import HTTPException

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    except:
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        if db:
            db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_holiday():
    holiday = {"date": "2022-01-01", "desc": "New Year's Day"}
    response = client.post("/holiday/", json=holiday)
    assert response.status_code == 200
    assert response.json()["date"] == holiday["date"]
    assert response.json()["desc"] == holiday["desc"]

def test_get_all_holidays():
    response = client.get("/holidays/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_check_date_is_holiday():
    response = client.get("/check/holiday/date/2022-01-01")
    assert response.status_code == 200
    assert response.json()["is_holiday"] == True

def test_get_holiday_by_desc():
    response = client.get("/holiday/desc/New Year's Day")
    assert response.status_code == 200
    assert response.json()["desc"] == "New Year's Day"

def test_delete_holiday():
    holiday = {"date": "2022-01-02", "desc": "New Year's Day Observed"}
    response = client.post("/holiday/", json=holiday)
    holiday_id = response.json()["id"]
    response = client.delete(f"/holiday/{holiday_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "record has been deleted"}

def test_create_holidays():
    holidays = {"data": [{"date": "2022-02-14", "desc": "Valentine's Day"}, {"date": "2022-07-04", "desc": "Independence Day"}]}
    response = client.post("/holidays/", json=holidays)
    assert response.status_code == 200
    assert response.json() == {"message": "successfully bulk inserted"}