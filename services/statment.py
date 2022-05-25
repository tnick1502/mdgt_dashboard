import re
from dataclasses import dataclass
from datetime import datetime, date
import os
import threading
from database import Session
import time

from typing import Dict, List


import xlrd
from xlrd import open_workbook
from models.reports import Report
from services.reports import ReportsService
import tables


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

class Statment:
    """Класс хранит всю ведомость выданных протоколов"""
    data: Dict[datetime, List[Unit]] = {}
    path: str = ""

    def __init__(self, path):
        self.set_excel_statment_path(path)
        self.data = {
            datetime(year=2019, month=1, day=1): [
                Unit(object_number="705-32", engineer="Михайлов А.И.",
                     mathcad_report=0, python_compression_report=0, python_report=0, python_dynamic_report=0,
                     plaxis_report=0, physical_statement=0, mechanics_statement=0),
                Unit(object_number="356-46", engineer="Жмылев Д.А.",
                     mathcad_report=0, python_compression_report=0, python_report=0, python_dynamic_report=0,
                     plaxis_report=0, physical_statement=0, mechanics_statement=0),
            ],
            datetime(year=2019, month=2, day=1): [
                Unit(object_number="705-32", engineer="Михайлов А.И.",
                     mathcad_report=0, python_compression_report=0, python_report=0, python_dynamic_report=0,
                     plaxis_report=0, physical_statement=0, mechanics_statement=0),
                Unit(object_number="356-46", engineer="Жмылев Д.А.",
                     mathcad_report=0, python_compression_report=0, python_report=0, python_dynamic_report=0,
                     plaxis_report=0, physical_statement=0, mechanics_statement=0),
            ]
        }
        my_thread = threading.Thread(target=self.update, args=())
        my_thread.start()

    def set_excel_statment_path(self, path: str):
        if os.path.isfile(path) and path.endswith("xls"):
            self.path = path
        else:
            print("Check file path")

    def update(self):
        """Подгрузка файла ведомости"""
        while True:
            if self.path:
                data = Statment.read_excel_statment(self.path)
                if data != self.data:
                    self.data = dict(data)
                    self.update_reports()
                time.sleep(5)
            else:
                assert()

    def get_month_count(self, date: datetime):
        result: Dict = {}

        if date not in self.data.keys():
            return result

        for unit in self.data[date]:
            reports = unit.get_reports()
            for report in reports:
                if report not in result.keys():
                    result[report] = reports[report]
                else:
                    result[report] += reports[report]

        return result

    def update_reports(self):
        now = datetime.now()
        res = self.get_month_count(datetime(year=now.year, month=now.month, day=1))
        res["python_all"] = res['python_report'] + res['python_compression_report'] + res['python_dynamic_report']
        all = res["python_all"] + res['mathcad_report']
        res["date"] = date(year=now.year, month=now.month, day=25)
        if all:
            res["python_percent"] = round((res["python_all"]/all)*100, 2)
        else:
            res["python_percent"] = 0.0

        rep_data = Report(**res)
        session = Session()

        test_report = session.query(tables.Report).filter_by(date=res["date"]).first()
        if not test_report :
            report = tables.Report(**rep_data.dict())
            session.add(report)
            session.commit()
            session.close()
        else:
            for field, value in rep_data:
                setattr(test_report, field, value)
            session.commit()
            session.close()

    def base_full(self):
        for i in [1,2,3,4, 5]:
            res = self.get_month_count(datetime(year=2022, month=i, day=1))
            res["python_all"] = res['python_report'] + res['python_compression_report'] + res['python_dynamic_report']
            all = res["python_all"] + res['mathcad_report']
            res["date"] = date(year=2022, month=i, day=25)
            if all:
                res["python_percent"] = round((res["python_all"] / all) * 100, 2)
            else:
                res["python_percent"] = 0.0

            rep_data = Report(**res)
            session = Session()

            test_report = session.query(tables.Report).filter_by(date=res["date"]).first()
            if not test_report:
                report = tables.Report(**rep_data.dict())
                session.add(report)
                session.commit()
                session.close()
            else:
                for field, value in rep_data:
                    setattr(test_report, field, value)
                session.commit()
                session.close()

    def str_pay(self, date=None):
        if date is None:
            now = datetime.now()
        else:
            now = date
        #self.update()
        res = self.get_month_count(datetime(year=now.year, month=now.month, day=1))
        sum_now = (res['python_report'] + res['python_dynamic_report']) * 45
        sum_soon = ((res['python_report'] + res['python_dynamic_report'] + res['python_compression_report']) * 45) + (res['mechanics_statement']*9) + (res['physical_statement']*17.5) + (res['mathcad_report']*10)
        return f"""
Никита: {round(sum_soon*0.32)} руб
Стас: {round(sum_soon*0.2)} руб
Олеся: {round(sum_soon*0.2)} руб
Иван: {round(sum_soon*0.1)} руб
Дима Жмылев: {round(sum_soon*0.05)} руб
Ольга Васильевна: {round(sum_soon*0.05)} руб
Женя: {round(sum_soon*0.05)} руб
Дима: {round(sum_soon*0.03)} руб
"""

    @staticmethod
    def read_excel_statment(path: str) -> 'Statment.data':
        __result: 'Statment.data' = {}
        result: 'Statment.data' = {}

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
                return Statment.data

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

    def __repr__(self):
        return "\n".join(list(map(lambda key: f"{key.strftime('%d.%m.%Y')}: {repr(self.data[key])}", self.data)))

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

class Prize:
    def __init__(self, excel_directory):
        self._excel_directory = excel_directory
        self._prize = 0

    def get_current_prize(self):
        mounth, year = datetime.now().strftime('%m'), "20" +datetime.now().strftime('%y')

        try:
            path = os.path.join(
                f'{self._excel_directory}{year}',
                f'{mounth}.{year} - Учет офисного времени.xls')

            if os.path.exists(path):

                with xlrd.open_workbook(path) as workbook:
                    worksheet = workbook.sheet_by_name('Итог')
                    prize = worksheet.cell(0, 24).value

                if prize == "ххх" or prize == "xxx":
                    self._prize = 0.0
                else:
                    self._prize = float(prize)

            else:
                self._prize = 0.0

        except:
            print("4")
            self._prize = 0.0

    def update(self):
        prize = Prize.get_prize(datetime.now().strftime('%m'), datetime.now().strftime('%y'), self._excel_path)

        if prize in ["Премия не заполнена", "Нет файла", "Неверный запрос"]:
            return ""

        if float(prize) != float(self._prize):
            self._prize = prize
            self.save_json_prize()
            return self.prize_massage()
        else:
            return ""

    @staticmethod
    def get_prize(mounth, year, path):

        def test_m_y(mounth, year):
            if len(mounth) <= 1:
                mounth = "0" + mounth

            if len(year) <= 3:
                year = "20" + year
            return mounth, year

        mounth, year = test_m_y(mounth, year)

        try:
            path = f'{path}{year}/{mounth}.{year} - Учет офисного времени.xls'

            if os.path.exists(path):

                with xlrd.open_workbook(path) as workbook:
                    worksheet = workbook.sheet_by_name('Итог')
                    prize = worksheet.cell(0, 24).value

                if prize == "ххх" or prize == "xxx":
                    return "Премия не заполнена"
                else:
                    return str(prize)

            else:
                return "Нет файла"

        except:
            return "Неверный запрос"

if __name__ == "__main__":
    from settings import settings
    print(settings.statment_excel_path)
    #x = Statment(settings.statment_excel_path)
    s = Prize(settings.prize_directory)
    s.get_current_prize()
    print(s._prize)
    #print(x.str_pay())