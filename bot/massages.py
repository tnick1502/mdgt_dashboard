import random


class Massages():
    @staticmethod
    def fill_courses_and_tests_massage():
        return '''Заполните таблицы курсов, проделанных опытов и выданных протоколов
┈┈╭━━━━━╮┈┈┈┈┈
┈┈┃╭━━━╮┃┈┈┈┈┈
┈┈┃┃╭━╮┃┃┈◯◯┈┈
┈┈┃┃╰━━╯┃╭┻┻╮┈
┈╭┻┻━━━━┻╯◒◒┃┈
┈╰━━━━━━━━╰╯╯┈'''

    @staticmethod
    def happy_birthday_massage(name, phone_number):
        return """Сегодня празднует день рождения {name}
{phone_number}
┈┈┈☆☆☆☆☆☆☆☆☆┈┈┈
┈┈╭┻┻┻┻┻┻┻┻┻╮┈┈
┈┈┃╱╲╱╲╱╲╱╲╱┃┈┈
┈╭┻━━━━━━━━━┻╮┈
┈┃╱╲╱╲╱╲╱╲╱╲╱┃┈
┈┗━━━━━━━━━━━┛┈""".format(name=name, phone_number=phone_number)

    @staticmethod
    def start_massage():
        return """Привет. Я понимаю команды:

/help - покажет список команд,
/prize - покажет текущую премию,
/prizes - покажет все премии по месяцам,
/report - текушая статистика протоколов,
/reports - общая статистика протоколов,
/birthdays - дни рождения в текущем месяце

'Номер Олег' (имя или фамилия сотрудника в именительном падеже) - покажет номер сотрудника,
"""

    @staticmethod
    def congratulate_massage(holiday):
        cat = """
...........／＞　　フ
...........|　_　 _ l
.........／` ミ＿xノ мур
......../　　　　 |
......./　 ヽ　　 ﾉ
.... ..│　　|　|　|
...／￣|　　 |　|　|
...| (￣ヽ＿_ヽ_)__)
....＼二つ
"""

        owl = """
_______*_____*
______*_*****_*
_____*_(O)_(O)_*
____**____V____**
____**_________**
____**_________**
_____*_________*
______***___***
"""

        return """Сongratulation!
Happy {holiday}
{animal}
""".format(holiday=holiday, animal=random.choice([owl, cat]))

    @staticmethod
    def prize_massage(prize):
        if float(prize) < 50:
            return f"Премия {prize} ¯\_(ツ)_/¯"
        elif float(prize) < 100:
            return f"Премия {prize} (ง ͠° ͟ل͜ ͡°)ง"
        elif float(prize) < 150:
            return f"Премия {prize} ( ͡° ͜ʖ ͡°)"
        elif float(prize) < 200:
            return f"Премия {prize} ( ͡ᵔ ͜ʖ ͡ᵔ )"
        else:
            return f"Премия {prize} ＼(٥⁀▽⁀)／"