from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int
    city_id: int


class  TemperatureUpdate(TemperatureBase):
    id: int

class  Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int