from typing import List, Optional
from datetime import date
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.reports import Report

import db.tables as tables
from db.database import get_session

class ReportsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, date: date) -> Optional[tables.Report]:
        report = self.session.query(tables.Report).filter_by(date=date).first()
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return report

    def get_all(self) -> List[tables.Report]:
        reports = self.session.query(tables.Report).all()
        return reports

    def get(self, date: date) -> tables.Report:
        report = self._get(date)
        return report

    def create(self, report_data: Report) -> tables.Report:
        p_all = report_data.python_report + report_data.python_dynamic_report + report_data.python_compression_report
        all = p_all + report_data.mathcad_report

        if all:
            p_percent = round((p_all/all) * 100, 2)
        else:
            p_percent = 0.0

        try:
            self._get(report_data.date)
        except HTTPException:
            report = tables.Report(
                **report_data.dict(),
                python_all=p_all,
                python_percent=p_percent)
            self.session.add(report)
            self.session.commit()
            return report
        else:
            data = report_data.dict()
            data["python_all"] = p_all
            data["python_percent"] = p_percent
            report_data = Report(**data)
            return self.update(report_data.date, report_data)

    def update(self, date: date, report_data: Report) -> tables.Report:
        report = self._get(date)
        for field, value in report_data:
            setattr(report, field, value)
        self.session.commit()
        return report

    def delete(self, date: date):
        report = self._get(date)
        self.session.delete(report)
        self.session.commit()

    def create_many(self, reports_data: List[Report]) -> List[tables.Report]:
        reports = [tables.Report(**report_data.dict()) for report_data in reports_data]
        self.session.add_all(reports)
        self.session.commit()
        return reports


