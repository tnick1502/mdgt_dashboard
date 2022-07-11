import datetime

from aiogram import Bot, Dispatcher, executor, types, utils
from dotenv import load_dotenv
from massages import Massages
import os
from io import BytesIO
from datetime import date
import aiohttp
import asyncio
import json
import aioschedule
import emoji

load_dotenv(dotenv_path=os.path.normpath(".env"))

API_TOKEN = os.getenv('API_TOKEN')
MDGT_CHAT_ID = os.getenv('MDGT_CHAT_ID')
MDGT_CHANNEL_ID = os.getenv('MDGT_CHANNEL_ID')
SERVER_URI = os.getenv('SERVER_URI')
SERVER_CUSTOMER_URI = os.getenv('SERVER_CUSTOMER_URI')
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


async def get_respones(url: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()
    except (aiohttp.client_exceptions.ClientConnectorError, aiohttp.client_exceptions.ContentTypeError):
        return None

async def get_respones_with_auth(url: str):
    jar = aiohttp.CookieJar(unsafe=True)
    try:
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

            async with session.get(url) as resp:
                return await resp.json()
    except aiohttp.client_exceptions.ClientConnectorError:
        return None

async def download_content_as_bytes(url: str) -> bytes:
    content = None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()
    except aiohttp.client_exceptions.ClientConnectorError:
        pass
    finally:
        return content


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.answer(Massages.start_massage())

@dp.message_handler(commands=["prize"])
async def prize(message: types.Message):
    """Запрос текущей премии"""
    today = date.today()
    prize = await get_respones(f'{SERVER_URI}/prizes/{today.year}-{today.month}-25')
    if prize is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

    await message.answer(f"{prize.get('prize', 0)} %")

@dp.message_handler(commands=["prizes"])
async def prizes(message: types.Message):
    """Запрос истории премий"""
    prizes = await get_respones(f'{SERVER_URI}/prizes/')
    if prizes is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

    try:
        s = "".join([f"дата: {prize['date']} | премия: {prize['prize']}\n" for prize in prizes])
        await message.answer(s if s else "Не найдено")
    except:
        await message.answer("Не найдено")

@dp.message_handler(commands=["report"])
async def report(message: types.Message):
    """Запрос отчета за текущий месяц"""
    today = date.today()
    report = await get_respones(f'{SERVER_URI}/reports/{today.year}-{today.month}-25')
    if report is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

    if 'detail' in report:
        await message.answer("Не найдено")
    else:
        s = "\n".join([f"{key}: {report[key]}" for key in report.keys() if key != "date"])
        await message.answer(s)

@dp.message_handler(commands=["reports"])
async def reports(message: types.Message):
    """Запрос истории отчетности"""
    reports = await get_respones(f'{SERVER_URI}/reports/')
    if reports is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

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
    pay = await get_respones_with_auth(f'{SERVER_URI}/pay/{today.year}-{today.month}-25')

    if pay is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

    if 'detail' in pay:
        await message.answer("Не найдено")
    else:
        s = "\n".join([f"{key}: {pay[key]}" for key in pay.keys() if key != "date"])
        await message.answer(s)

@dp.message_handler(commands=["pays"])
async def pays(message: types.Message):
    """Запрос статистики оплаты"""
    pays = await get_respones_with_auth(f'{SERVER_URI}/pay/')
    if pays is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

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
    staffs = await get_respones(f'{SERVER_URI}/staff/month_birthday/?month={today.month}')
    if staffs is None:
        await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
        return

    try:
        s = ""
        for staff in staffs:
            s += f"{staff['birthday']} | {staff['full_name']}" + "\n\n"
        await message.answer(s if s else "Не найдено")
    except:
        await message.answer("Не найдено")

@dp.message_handler(commands=["time"])
async def time(message: types.Message):
    """Запрос текущего времени"""
    await message.answer(datetime.datetime.now())

@dp.message_handler()
async def echo(message: types.Message):
    if message.text.upper().find('НОМЕР') != -1:
        name = message.text.split(" ")[1]
        staffs = await get_respones(f'{SERVER_URI}/staff/{name}')

        if staffs is None:
            await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
            return

        try:
            s = "".join([f"{staff['full_name']} | {staff['phone']}\n" for staff in staffs])
            await message.answer(s if s else "Не найдено")
        except:
            await message.answer("Не найдено")

    elif message.text.upper().find('ЗАКАЗЧИК') != -1:
        name = message.text.split(" ")[1]

        customers = await get_respones(f'{SERVER_CUSTOMER_URI}/customers/{name}')

        if customers is None:
            await message.answer(text="Сервер не отвечает " + emoji.emojize(":smiling_face_with_tear:"))
            return

        if len(customers):
            for customer in customers:
                s = f"ФИО: {customer['full_name']}\nНомер телефона: +{customer['phone_number']}\nПочта: {customer['email']}\nОрганизация: {customer['organization']}\nДата рождения: {customer['birthday']}\n"
                photo = await download_content_as_bytes(f'{SERVER_CUSTOMER_URI}/customers/get_photo/{customer["id"]}')
                try:
                    bytes_photo = BytesIO()
                    bytes_photo.write(photo)
                    bytes_photo.seek(0)
                    await bot.send_photo(message.from_user.id, types.InputFile(bytes_photo), caption=s)
                except utils.exceptions.BadRequest:
                    await message.answer(s)
        else:
            await message.answer("Не найдено")


async def scheduler():

    async def check_prize():
        global saved_prize
        today = date.today()
        prize = await get_respones(f'{SERVER_URI}/prizes/{today.year}-{today.month}-25')
        try:
            prize = prize.get('prize', 0)
            if prize != saved_prize:
                saved_prize = prize
                save_json_prize(prize)
                await bot.send_message(MDGT_CHANNEL_ID, text=Massages.prize_massage(prize))
        except TypeError:
            pass

    async def check_birthday():
        today = date.today()
        staffs = await get_respones(f'{SERVER_URI}/staff/day_birthday/?month={today.month}&day={today.day}')
        try:
            for staff in staffs:
                if staff == "detail":
                    return
                await bot.send_message(MDGT_CHANNEL_ID,
                                      text=Massages.happy_birthday_massage(staff["full_name"], staff["phone"]))
        except TypeError:
            pass

    aioschedule.every(10).minutes.do(check_prize)
    aioschedule.every().day.at("9:30").do(check_birthday)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)