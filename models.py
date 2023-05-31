from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
import uuid
from database import Base


class Holiday(Base):
    __tablename__ = "holidays"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid1()), unique=True)
    date = Column(String)
    desc = Column(String)

    class Config:
        orm_mode = True