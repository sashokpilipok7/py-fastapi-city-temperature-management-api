from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class  TemperatureUpdate(TemperatureBase):
    pass

class  Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int