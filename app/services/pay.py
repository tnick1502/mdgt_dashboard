from services.reports import ReportsService, date, Optional
import db.tables as tables

persons = {
    "Тишин Н.Р.": 0.32,
    "Доронин С.А.": 0.2,
    "Селиванова О.С.": 0.2,
    "Селиванов И.А.": 0.1,
    "Жмылев Д.А.": 0.05,
    "Семенова О.В.": 0.05,
    "Горшков Е.С.": 0.05,
    "Смирнов Д.А.": 0.03,
}

tips = {
    'python_report': 45,
    'python_dynamic_report': 45,
    'python_compression_report': 45,
    'mechanics_statement': 9,
    'physical_statement': 17.5,
    'mathcad_report': 10
}

class PayService(ReportsService):
    def get_pay(self):
        reports = self.get_all()
        return [PayService.convert(report) for report in reports]

    def get_one_pay(self, date: Optional[date]):
        if date:
            report = self._get(date)
            return PayService.convert(report)

    @staticmethod
    def convert(report: tables.Report):
        if not report:
            return {
                key: "0 руб" for key in persons
            }

        sum = report.python_report * tips["python_report"] + \
              report.python_dynamic_report * tips["python_dynamic_report"] + \
              report.python_compression_report * tips["python_compression_report"] + \
              report.mathcad_report * tips["mathcad_report"] + \
              report.physical_statement * tips["physical_statement"] + \
              report.mechanics_statement * tips["mechanics_statement"]

        res = {
            key: round(persons[key]*sum) for key in persons.keys()
        }

        res["data"] = report.date

        return res