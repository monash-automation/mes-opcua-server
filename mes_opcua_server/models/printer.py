from datetime import datetime
from ipaddress import IPv4Address

from opcuax import OpcuaModel
from pydantic import BaseModel, Field, NonNegativeFloat


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
    ip: IPv4Address = "127.0.0.1"
    last_update: datetime = Field(default_factory=datetime.now)

    state: str = "N/A"
    nozzle: Temperature = Temperature()
    bed: Temperature = Temperature()
    head: PrinterHead = PrinterHead()
    job: PrinterJob = PrinterJob()
