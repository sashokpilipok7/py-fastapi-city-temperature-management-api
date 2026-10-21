from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from database import Base

class DBTemperature(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    temperature = Column(Integer)

    city_id = Column(Integer, ForeignKey('cities.id'))