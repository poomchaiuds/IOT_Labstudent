from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship

from database import Base

class Student(Base):
    __tablename__ = 'students'

    fname = Column(String, index=True)
    lname = Column(String, index=True)
    id = Column(Integer, primary_key=True, index=True)
    born = Column(String, index=True)
    gender = Column(String, index=True)

