from pydantic import BaseModel
from typing import List, Optional


class Holiday(BaseModel):
    date: str
    desc: str

    class Config:
        orm_mode = True

class HolidayResponse(BaseModel):
    date: str
    desc: str
    id: str

    class Config:
        orm_mode = True


class HolidayList(BaseModel):
    data: List[Holiday]

    class Config:
        orm_mode = True


class HolidayDelete(BaseModel):
    id: str


class HolidayCheck(BaseModel):
    holiday: Optional[Holiday]
    is_holiday: bool
