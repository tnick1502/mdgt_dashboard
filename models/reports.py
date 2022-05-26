from pydantic import BaseModel
from datetime import date

class ReportBase(BaseModel):
    date: date
    python_report: int
    python_dynamic_report: int
    python_compression_report: int
    mathcad_report: int
    physical_statement: int
    mechanics_statement: int

    class Config:
        orm_mode = True

class Report(ReportBase):
    python_all: float
    python_percent: float

class ReportCreate(ReportBase):
    pass
