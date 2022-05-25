from typing import List, Optional
from datetime import date
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.prizes import Prize

import tables
from database import get_session

class PrizesService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, date: date) -> Optional[tables.Prize]:
        prize = self.session.query(tables.Prize).filter_by(date=date).first()
        if not prize:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return prize

    def get_all(self) -> List[tables.Prize]:
        prizes = self.session.query(tables.Prize).all()
        return prizes

    def get(self, date: date) -> tables.Prize:
        self._get(date)

    def create(self, prize_data: Prize) -> tables.Prize:
        prize = tables.Prize(**prize_data.dict())
        try:
            self._get(prize_data.date)
        except HTTPException:
            self.session.add(prize)
            self.session.commit()
            return prize
        else:
            return self.update(prize.date, prize_data)

    def update(self, date: date, prize_data: Prize) -> tables.Prize:
        prize = self._get(date)
        for field, value in prize_data:
            setattr(prize, field, value)
        self.session.commit()
        return prize

    def delete(self, date: date):
        prize = self._get(date)
        self.session.delete(prize)
        self.session.commit()

    def create_many(self, prizes_data: List[Prize]) -> List[tables.Prize]:
        prizes = [tables.Report(**prize_data.dict()) for prize_data in prizes_data]
        self.session.add_all(prizes)
        self.session.commit()
        return prizes
