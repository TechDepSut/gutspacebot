import os
import asyncio
from vkbottle import Bot, Keyboard, Text
from vkbottle import BaseStateGroup, KeyboardButtonColor
from vkbottle.bot import Message
from utils.bookingtime import *
from utils.sheetsconnect import *

bot = Bot(os.environ["token"])


class Branch(BaseStateGroup):
    HELLO = 0
    BOOKING = 1
    QUESTION = 2
    BOOKINGEND = 3


@bot.on.message(text="Начать")
async def start(m: Message) -> None:
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Бронь"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Задать вопрос"), color=KeyboardButtonColor.PRIMARY)
    await m.answer("Выбери действие", keyboard=keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.HELLO)


@bot.on.message(state=Branch.HELLO, text="Бронь")
async def reg(m: Message) -> None:
    await m.answer(
        "Чтобы сделать бронь, необходимо пройти регистрацию. Для этого введи ФИО"
    )
    await bot.state_dispenser.set(m.peer_id, Branch.BOOKING)


@bot.on.message(state=Branch.BOOKING)
async def time(m: Message) -> None:
    btime = await timebuttons()
    if len(btime) == 0:
        await m.answer("Извини, но все места в ближайшее время заняты, или коворкинг сейчас не работает")
    else:
        keyboard = Keyboard(one_time=True)
        for i in btime:
            keyboard.add(Text(i), color=KeyboardButtonColor.PRIMARY)
        await m.answer(
            "Отлично! Теперь выбери удобное время для сеанса. Напоминаем, что один сеанс длится 2 часа.",
            keyboard=keyboard,
        )
    await bot.state_dispenser.set(m.peer_id, Branch.BOOKINGEND, name=str(m.text))


@bot.on.message(state=Branch.BOOKINGEND)
async def bookingComplete(m: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Бронь"), color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Задать вопрос"), color=KeyboardButtonColor.PRIMARY)
    if await bookingCheck(m.text, m.peer_id):
        await m.answer("Ты уже зарегестрирован на это время", keyboard=keyboard)
    else:
        await bookingDB(m.text)
        await m.answer(
            "Ждем тебя в SutSpace! За 15 минут до окончания твоего сеанса бот вышлет тебе напоминание.",
            keyboard=keyboard,
        )
        await person_add(m.state_peer.payload["name"], str(m.text))
        global stop_polling_sheet
        stop_polling_sheet = asyncio.Event()
        while True:
            try:
                await asyncio.wait_for(stop_polling_sheet.wait(), timeout=10)
            except asyncio.TimeoutError:
                try:
                    await m.answer("До окончания твоего сеанса осталось 15 минут")
                    break
                except:
                    print("Not working")
    await bot.state_dispenser.set(m.peer_id, Branch.HELLO)


@bot.on.message(state=Branch.HELLO, text="Задать вопрос")
async def question(m: Message) -> None:
    await m.answer("Задай свой вопрос")
    await bot.state_dispenser.set(m.peer_id, Branch.QUESTION)


@bot.on.message(state=Branch.QUESTION)
async def questionComplete(m: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text("Бронь"), color=KeyboardButtonColor.PRIMARY)
    await m.answer(
        "Спасибо за обращение! Совсем скоро администратор коворкинга ответит тебе.",
        keyboard=keyboard,
    )
    await bot.state_dispenser.set(m.peer_id, Branch.HELLO)


if __name__ == "__main__":
    bot.run_forever()
