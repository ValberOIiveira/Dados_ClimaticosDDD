from pydantic import BaseModel


class CityData(BaseModel):
    cidade: str

class WeatherDataBase(BaseModel):
    city: str
    country: str
    temperature: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_deg: int
    description: str
    visibility: int
    sunrise: str
    sunset: str
    timestamp: str


class WeatherDataCreate(WeatherDataBase):
    pass


class WeatherData(WeatherDataBase):
    id: int

    class Config:
        orm_mode = True
