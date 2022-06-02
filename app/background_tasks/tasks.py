import re
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from dateutil import rrule
from passlib.hash import bcrypt
from pydantic import ValidationError
import os
from db.database import Session
from typing import Dict
import xlrd
from xlrd import open_workbook
from loguru import logger
import time

from models.reports import Report
from models.prizes import Prize
import db.tables as tables
from tqdm import tqdm

@dataclass
class Unit:
    """Класс хранит одну строчку с выданными протоколами и ведомостями по объекту"""
    object_number: str = None
    engineer: str = "unknown"
    mathcad_report: int = 0
    python_compression_report: int = 0
    python_report: int = 0
    python_dynamic_report: int = 0
    plaxis_report: int = 0
    physical_statement: int = 0
    mechanics_statement: int = 0

    def __repr__(self):
        return f"\n\t\t\tОбъект: {self.object_number}, Исполнитель: {self.engineer}," \
               f" Протоколы: Маткад - {self.mathcad_report}, Python Компрессия - {self.python_compression_report}," \
               f" Python Другое - {self.python_report}, Python Динамика - {self.python_dynamic_report}," \
               f" Plaxis - {self.plaxis_report};" \
               f" Ведомости: Механика - {self.mechanics_statement}, Физика - {self.physical_statement}"

    def get_reports(self):
        return {'mathcad_report': self.mathcad_report, 'python_compression_report': self.python_compression_report,
                'python_report': self.python_report, 'python_dynamic_report': self.python_dynamic_report,
                'plaxis_report': self.plaxis_report, 'physical_statement': self.physical_statement,
                'mechanics_statement': self.mechanics_statement}

class XlsBook:
    """
    Convenience class for xlrd xls reader (only read mode)
    Note: Methods imputes operates with Natural columns and rows indexes
    """

    book = None
    sheet = None

    __sheet_index: int

    def __init__(self, path: str):
        self.set_book(path)

    def set_book(self, path: str):
        assert path.endswith('.xls'), 'Template should be .xls file format'
        self.book = open_workbook(path, formatting_info=True)
        self.set_sheet_by_index(0)

    def set_sheet_by_index(self, index: int):
        self.sheet = self.book.sheet_by_index(index)
        self.__sheet_index = index

    def set_next_sheet(self):
        _last_sheet_index = self.sheet_count() - 1
        if self.__sheet_index < _last_sheet_index:
            self.set_sheet_by_index(self.__sheet_index + 1)

    def is_empty_sheet(self, min_cols: int = 1, min_rows: int = 1) -> bool:
        if self.sheet.ncols < min_cols or self.sheet.nrows < min_rows:
            return True
        return False

    def get_sheet_index(self) -> int:
        return self.__sheet_index

    def sheet_count(self) -> int:
        return len(self.book.sheet_names())

    def sheet_names(self) -> list:
        return self.book.sheet_names()

    def cell_value(self, natural_row: int, natural_column: int):
        return self.sheet.cell(natural_row - 1, natural_column - 1).value

    def cell_value_int(self, natural_row: int, natural_column: int) -> int:
        value = self.cell_value(natural_row, natural_column)
        try:
            return int(value)
        except ValueError:
            return 0

    def cell_value_date(self, natural_row: int, natural_column: int):
        MARKS = ['/', ' ', ',']

        value = str(self.cell_value(natural_row, natural_column))

        if not value.replace(' ', ''):
            return None

        if self.cell_value_int(natural_row, natural_column):
            value = self.cell_value_int(natural_row, natural_column)
            return xlrd.xldate_as_datetime(value, 0)

        for mark in MARKS:
            if mark in value:
                value = value.replace(mark, '.')

        if re.fullmatch(r'[0-9]{2}[.][0-9]{2}[.][0-9]{4}', value):
            try:
                return datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                pass
        if re.fullmatch(r'[0-9]{2}[.][0-9]{2}[.][0-9]{2}', value):
            try:
                return datetime.strptime(value, '%d.%m.%y').date()
            except ValueError:
                pass

        return None

    def cell_back_color(self, natural_row: int, natural_column: int):
        row = natural_row - 1
        col = natural_column - 1
        cell = self.sheet.cell(row, col)
        xf = self.book.xf_list[cell.xf_index]
        if not xf.background:
            return None
        return self.__get_color(xf.background.pattern_colour_index)

    def cell_front_color(self, natural_row: int, natural_column: int):
        row = natural_row - 1
        col = natural_column - 1
        cell = self.sheet.cell(row, col)
        xf = self.book.xf_list[cell.xf_index]
        font = self.book.font_list[xf.font_index]
        if not font:
            return None
        return self.__get_color(font.colour_index)

    def __get_color(self, color_index: int):
        return self.book.colour_map.get(color_index)

def prize_parser(excel_directory: str, current_date: date = date.today()):

    def get_current_prize(excel_directory, current_date):
        mounth, year = current_date.strftime('%m'), "20" + current_date.strftime('%y')

        try:
            path = os.path.join(
                f'{excel_directory}{year}',
                f'{mounth}.{year} - Учет офисного времени.xls')

            if os.path.exists(path):

                with xlrd.open_workbook(path) as workbook:
                    worksheet = workbook.sheet_by_name('Итог')
                    prize = worksheet.cell(0, 24).value

                if prize == "ххх" or prize == "xxx":
                    prize = 0.0
                else:
                    prize = float(prize)

            else:
                prize = 0.0

        except:
            prize = 0.0

        return prize

    def update_run(excel_dir, base_prize, current_date):
        prize = get_current_prize(excel_dir, current_date)

        if prize > base_prize:
            data = {
                "date": date(year=current_date.year, month=current_date.month, day=25),
                "prize": prize,
            }

            prize_data = Prize(**data)

            test = _get(date=prize_data.date)

            if test is not None:
                update(data=prize_data)
            else:
                create(data=prize_data)

    def _get(date: date) -> tables.Prize:
        session = Session()
        prize = session.query(tables.Prize).filter_by(date=date).first()
        session.close()
        return prize

    def update(data: Prize) -> None:
        session = Session()
        prize = session.query(tables.Prize).filter_by(date=data.date).first()
        for field, value in data:
            setattr(prize, field, value)
        session.commit()
        session.close()

    def create(data: Prize) -> None:
        session = Session()
        session.add(tables.Prize(**data.dict()))
        session.commit()
        session.close()

    if not os.path.exists(excel_directory):
        raise FileNotFoundError("Отсутствует файл премии")

    _excel_directory = excel_directory

    base_prize = _get(date(year=current_date.year, month=current_date.month, day=25))

    if not base_prize:
        _prize = 0.0
    else:
        _prize = base_prize.prize

    update_run(_excel_directory, _prize, current_date)

def report_parser(excel_path: str, current_date: date = date.today()):

    def get_month_count(main_data, date: datetime):
        result: Dict = {}

        if date not in main_data.keys():
            return result

        for unit in main_data[date]:
            reports = unit.get_reports()
            for report in reports:
                if report not in result.keys():
                    result[report] = reports[report]
                else:
                    result[report] += reports[report]

        return result

    def update_reports(statment_data, base_report_data, current_date):
        res = get_month_count(statment_data, datetime(year=current_date.year, month=current_date.month, day=1))
        if res:
            res["python_all"] = res['python_report'] + res['python_compression_report'] + res['python_dynamic_report']
            all = res["python_all"] + res['mathcad_report']
            res["date"] = date(year=current_date.year, month=current_date.month, day=25)
            if all:
                res["python_percent"] = round((res["python_all"] / all) * 100, 2)
            else:
                res["python_percent"] = 0.0

            if base_report_data.dict() != res:

                rep_data = Report(**res)

                test = _get(date=rep_data.date)

                if test is not None:
                    update(data=rep_data)
                else:
                    create(data=rep_data)

    def read_excel_statment(path: str) -> 'ReportParser.data':
        __result: 'ReportParser.data' = {}
        result: 'ReportParser.data' = {}

        # colors
        YELLOW = (255, 255, 0)

        # program local columns shifts (natural local column - 'Object' column): 2 - 1 = 1 and so on
        # reports
        MATHCAD = 1  # Mathcad
        PYTHON_COMPRESSION = 2  # Python Компрессия
        PYTHON = 3  # Python Другое
        PYTHON_DYNAMIC = 4  # Python Динамика
        PLAXIS = 5  # Plaxis
        # Statements
        MECHANICS = 6  # Механика
        PHYSICAL = 7  # Физика

        # local columns per engineer
        N_COLS = 9
        '''cols count per engineer'''

        # first month row
        START_ROW = 6

        # if no last date in xls start date will be used
        start_date = datetime(year=2017, month=2, day=1)

        last_date = None
        '''last defined in xls date is the last date overall'''

        def next_month(_date):
            month = _date.month
            if month + 1 == 13:
                return datetime(year=_date.year + 1, month=1, day=1)
            return datetime(year=_date.year, month=month + 1, day=1)

        def prev_month(_date):
            month = _date.month
            if month - 1 == 0:
                return datetime(year=_date.year - 1, month=12, day=1)
            return datetime(year=_date.year, month=month - 1, day=1)

        # load book
        book = XlsBook(path)

        # engineers
        engineers = []
        engineers_row = 1

        def engineer(natural_col: int):
            """Returns engineer name by natural column index"""
            __col = natural_col - 1
            if __col // N_COLS >= len(engineers):
                return None
            return engineers[__col // N_COLS]

        # start parsing for each sheet
        while not book.is_empty_sheet(min_rows=START_ROW, min_cols=N_COLS):
            # count sheet sizes
            ncols = book.sheet.ncols + 1  # Natural ncols
            nrows = book.sheet.nrows + 1  # Natural nrows

            # fill-in engineers
            engineers = []
            for col in range(ncols):
                curr_engineer = book.cell_value(engineers_row, col)
                if curr_engineer in engineers:
                    continue
                if len(curr_engineer) > 0:
                    engineers.append(curr_engineer)
            if len(engineers) < 1:  # no engineers = no data
                return {}

            # for each row (read comments)
            for row in range(START_ROW, nrows):
                # search for date (YELLOW line)
                dates = [*__result.keys()]
                if book.cell_back_color(row, 1) == YELLOW:

                    # save the last date
                    for col in range(1, ncols):
                        value = book.cell_value_date(row, col)
                        if value:
                            last_date = value

                    # fill in base dates to recalculate them later by last_date
                    if dates:
                        __result[next_month(dates[-1])] = []
                    else:
                        __result[start_date] = []
                    continue

                if not dates:
                    continue

                # skip the summarize row
                if book.cell_value(row, 1) == "Сумма":
                    continue

                # then parse columns per each engineer
                for col in range(1, ncols + 1, N_COLS):

                    _object = book.cell_value(row, col).replace(' ', '')

                    # first one should find out if there any object (per each engineer)
                    if not engineer(col) or not _object:
                        continue

                    if col + MECHANICS > ncols:
                        continue

                    # read numbers (per each engineer)
                    _mathcad_count = book.cell_value_int(row, col + MATHCAD)
                    _python_compression_count = book.cell_value_int(row, col + PYTHON_COMPRESSION)
                    _python_count = book.cell_value_int(row, col + PYTHON)
                    _python_dynamic_count = book.cell_value_int(row, col + PYTHON_DYNAMIC)
                    _plaxis_count = book.cell_value_int(row, col + PLAXIS)
                    _mechanics_count = book.cell_value_int(row, col + MECHANICS)
                    _physical_count = book.cell_value_int(row, col + PHYSICAL)

                    # add to result (per each engineer)
                    __result[dates[-1]].append(Unit(object_number=str(_object), engineer=engineer(col),
                                                    mathcad_report=_mathcad_count,
                                                    python_compression_report=_python_compression_count,
                                                    python_report=_python_count,
                                                    python_dynamic_report=_python_dynamic_count,
                                                    plaxis_report=_plaxis_count, physical_statement=_physical_count,
                                                    mechanics_statement=_mechanics_count))

            # and next sheet
            book.set_next_sheet()

        # recalculate dates
        if last_date:
            start_date = last_date

            for i in range(len(__result.keys())):
                start_date = prev_month(start_date)

            for date in __result.keys():
                if len([*result.keys()]) > 0:
                    result[next_month([*result.keys()][-1])] = __result[date]
                else:
                    result[next_month(start_date)] = __result[date]

        return result

    def _get(date: date) -> tables.Report:
        session = Session()
        report = session.query(tables.Report).filter_by(date=date).first()
        session.close()
        return report

    def update(data: Report) -> None:
        session = Session()
        report = session.query(tables.Report).filter_by(date=data.date).first()
        for field, value in data:
            setattr(report, field, value)
        session.commit()
        session.close()

    def create(data: Report) -> None:
        session = Session()
        session.add(tables.Report(**data.dict()))
        session.commit()
        session.close()

    if not os.path.exists(excel_path):
        raise FileNotFoundError("Отсутствует файл отчетов")

    _excel_path = excel_path

    base_report_data = _get(date(year=current_date.year, month=current_date.month, day=25))

    if not base_report_data:
        base_report_data = Report.parse_obj(
            {
                "date": -1,
                "python_report": -1,
                "python_dynamic_report": -1,
                "python_compression_report": -1,
                "mathcad_report": -1,
                "physical_statement":  -1,
                "mechanics_statement": -1,
                "python_all": -1,
                "python_percent": -1,
            }
        )
    else:
        base_report_data = Report.from_orm(base_report_data)

    statment_data = read_excel_statment(excel_path)
    update_reports(statment_data, base_report_data, current_date)


#@dramatiq.actor
def parser(excel_directory, excel_path, date_delay=3, deelay=10, print=True):
    time.sleep(deelay)
    while True:
        current_date = date.today() - timedelta(days=date_delay)
        try:
            prize_parser(excel_directory, current_date)
            if print:
                logger.info("successful update prize")
        except Exception as err:
            logger.error("Ошибка обновления премии " + str(err))

        try:
            report_parser(excel_path, current_date)
            if print:
                logger.info("successful update reports")
        except Exception as err:
            logger.error("Ошибка обновления отчетов " + str(err))

        time.sleep(deelay)

def update_db(excel_directory, excel_path):

    if not os.path.exists(excel_directory):
        raise FileNotFoundError("Отсутствует файл премии")

    if not os.path.exists(excel_path):
        raise FileNotFoundError("Отсутствует файл отчетов")

    reports_dates = [
        date(year=dt.year, month=dt.month, day=25) for dt in rrule.rrule(
            rrule.MONTHLY, dtstart=date(2022, 1, 1), until=date.today()
        )]

    prize_dates = [
        date(year=dt.year, month=dt.month, day=25) for dt in rrule.rrule(
            rrule.MONTHLY, dtstart=date(2020, 5, 1), until=date.today()
        )]

    for d_p in tqdm(prize_dates):
        try:
            prize_parser(excel_directory, d_p)
            #logger.info(f"load prize {d_p} id db")
        except Exception as err:
            logger.error("Ошибка обновления премии " + str(err))

    for d_r in tqdm(reports_dates):
        try:
            report_parser(excel_path, d_r)
            #logger.info(f"load reports {d_p} id db")
        except Exception as err:
            logger.error("Ошибка обновления отчетов " + str(err))

def create_admin():
    session = Session()
    user = session.query(tables.User).filter_by(username="mdgt").first()
    session.close()

    if not user:
        session = Session()

        user = tables.User(
            username="mdgt",
            password_hash=bcrypt.hash("mdgt"),
        )

        session.add(user)
        session.commit()
        session.close()




if __name__ == "__main__":
    from settings import settings
    #parser(settings.prize_directory, settings.statment_excel_path)
    report_parser(settings.statment_excel_path)
    #prize_parser(settings.prize_directory)
