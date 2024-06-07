from sqlalchemy import Column, Integer, String, Float
from database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    country = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(Float)
    wind_deg = Column(Integer)
    description = Column(String)
    visibility = Column(Integer)
    sunrise = Column(String)
    sunset = Column(String)
    timestamp = Column(String)
