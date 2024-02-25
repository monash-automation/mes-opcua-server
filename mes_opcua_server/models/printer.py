from datetime import datetime

from opcuax import OpcuaModel
from pydantic import BaseModel, Field, HttpUrl, NonNegativeFloat


class PrinterHead(BaseModel):
    x: float = 0
    y: float = 0
    z: float = 0


class PrinterJob(BaseModel):
    file: str = "N/A"
    progress: NonNegativeFloat = 0
    time_left: NonNegativeFloat = 9999
    time_left_approx: NonNegativeFloat = 9999
    time_used: NonNegativeFloat = 0


class Temperature(BaseModel):
    actual: NonNegativeFloat = 0
    target: NonNegativeFloat = 0


class Printer(OpcuaModel):
    url: HttpUrl = "http://localhost"
    update_time: datetime = Field(default_factory=datetime.now)

    state: str = Field(default="N/A", examples=["ready", "printing", "error"])
    nozzle: Temperature = Temperature()
    bed: Temperature = Temperature()
    head: PrinterHead = PrinterHead()
    job: PrinterJob = PrinterJob()
    camera_url: HttpUrl = Field(
        default="http://localhost", examples=["http://172.32.1.92:8080/?action=stream"]
    )
    model: str = Field(default="Unknown", examples=["Prusa XL 1 head"])
