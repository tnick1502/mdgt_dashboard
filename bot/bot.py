from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from massages import Massages
import os
from datetime import date
import aiohttp
import requests
import asyncio
import json
import aioschedule

load_dotenv(dotenv_path=os.path.normpath(".env"))

API_TOKEN = os.getenv('API_TOKEN')
MDGT_CHAT_ID = os.getenv('MDGT_CHAT_ID')
MDGT_CHANNEL_ID = os.getenv('MDGT_CHANNEL_ID')
SERVER_URI = os.getenv('SERVER_URI')
SERVER_USERNAME = os.getenv('SERVER_USERNAME')
SERVER_PASSWORD = os.getenv('SERVER_PASSWORD')


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def save_json_prize(prize: float):
    """Сохраняет премию в  JSON"""
    with open("prize.json", 'w', encoding='utf-8') as file:
        json.dump({"prize": prize}, file)

def read_json_prize():
    """Читает JSON в словарь питон"""
    if os.path.exists("prize.json"):
        with open("prize.json", 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return json_data["prize"]
    else:
        save_json_prize(0)
        return 0

saved_prize = read_json_prize()


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.answer(Massages.start_massage())

@dp.message_handler(commands=["prize"])
async def prize(message: types.Message):
    """Запрос текущей премии"""
    today = date.today()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{SERVER_URI}/prizes/{today.year}-{today.month}-25') as resp:
            prize = await resp.json()
            await message.answer(f"{prize.get('prize', 0)} %")

@dp.message_handler(commands=["prizes"])
async def prizes(message: types.Message):
    """Запрос истории премий"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{SERVER_URI}/prizes/') as resp:
            prizes = await resp.json()
            try:
                s = "".join([f"дата: {prize['date']} | премия: {prize['prize']}\n" for prize in prizes])
                await message.answer(s if s else "Не найдено")
            except:
                await message.answer("Не найдено")

@dp.message_handler(commands=["report"])
async def report(message: types.Message):
    """Запрос отчета за текущий месяц"""
    today = date.today()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{SERVER_URI}/reports/{today.year}-{today.month}-25') as resp:
            report = await resp.json()
            if 'detail' in report:
                await message.answer("Не найдено")
            else:
                s = "\n".join([f"{key}: {report[key]}" for key in report.keys() if key != "date"])
                await message.answer(s)

@dp.message_handler(commands=["reports"])
async def reports(message: types.Message):
    """Запрос истории отчетности"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{SERVER_URI}/reports/') as resp:
            reports = await resp.json()
            try:
                s = ""
                for report in reports:
                    s += "\n".join([f"{key}: {report[key]}" for key in report.keys()]) + "\n\n\n"
                await message.answer(s if s else "Не найдено")
            except:
                await message.answer("Не найдено")

@dp.message_handler(commands=["pay"])
async def pay(message: types.Message):
    """Запрос оплаты за тукущий месяц"""
    today = date.today()
    jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        res = await session.post(f'{SERVER_URI}/authorization/sign-in/',
                                 data={
                                     "username": SERVER_USERNAME,
                                     "password": SERVER_PASSWORD,
                                     "grant_type": "password",
                                     "scope": "",
                                     "client_id": "",
                                     "client_secret": ""
                                 }, allow_redirects=False)
        await res.json()

        async with session.get(f'{SERVER_URI}/pay/{today.year}-{today.month}-25') as resp:
            pay = await resp.json()

            if 'detail' in pay:
                await message.answer("Не найдено")
            else:
                s = "\n".join([f"{key}: {pay[key]}" for key in pay.keys() if key != "date"])
                await message.answer(s)

@dp.message_handler(commands=["pays"])
async def pays(message: types.Message):
    """Запрос статистики оплаты"""
    jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        res = await session.post(f'{SERVER_URI}/authorization/sign-in/',
                                 data={
                                     "username": SERVER_USERNAME,
                                     "password": SERVER_PASSWORD,
                                     "grant_type": "password",
                                     "scope": "",
                                     "client_id": "",
                                     "client_secret": ""
                                 }, allow_redirects=False)
        await res.json()

        async with session.get(f'{SERVER_URI}/pay/') as resp:
            pays = await resp.json()
            try:
                s = ""
                for pay in pays:
                    s += "\n".join([f"{key}: {pay[key]}" for key in pay.keys()]) + "\n\n\n"
                await message.answer(s if s else "Не найдено")
            except:
                await message.answer("Не найдено")

@dp.message_handler(commands=["birthdays"])
async def birthdays(message: types.Message):
    """Запрос дней рождений в текущем месяцу"""
    today = date.today()
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{SERVER_URI}/staff/month_birthday/?month={today.month}') as resp:
            staffs = await resp.json()
            try:
                s = ""
                for staff in staffs:
                    s += f"{staff['birthday']} | {staff['full_name']}" + "\n\n"
                await message.answer(s if s else "Не найдено")
            except:
                await message.answer("Не найдено")

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.upper().find('НОМЕР') != -1:
        name = message.text.split(" ")[1]

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{"http://0.0.0.0:8000"}/staff/{name}') as resp:
                staffs = await resp.json()
                try:
                    s = "".join([f"{staff['full_name']} | {staff['phone']}\n" for staff in staffs])
                    await message.answer(s if s else "Не найдено")
                except:
                    await message.answer("Не найдено")


async def scheduler():

    async def check_prize():
        global saved_prize
        today = date.today()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{SERVER_URI}/prizes/{today.year}-{today.month}-25') as resp:
                prize = await resp.json()
                prize = prize.get('prize', 0)
                if prize != saved_prize:
                    saved_prize = prize
                    save_json_prize(prize)
                    await bot.send_message(MDGT_CHANNEL_ID, text=Massages.prize_massage(prize))

    async def check_birthday():
        today = date.today()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{SERVER_URI}/staff/day_birthday/?month={today.month}&day={today.day}') as resp:
                staffs = await resp.json()
                for staff in staffs:
                    if staff == "detail":
                        return
                    await bot.send_message(MDGT_CHANNEL_ID,
                                           text=Massages.happy_birthday_massage(staff["full_name"], staff["phone"]))

    aioschedule.every(10).minutes.do(check_prize)
    aioschedule.every().day.at("9:30").do(check_birthday)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)