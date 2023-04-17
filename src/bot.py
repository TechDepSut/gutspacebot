import os
from asyncio import sleep
from vkbottle import Bot, Keyboard, Text, API, LoopWrapper
from vkbottle import BaseStateGroup, KeyboardButtonColor
from vkbottle.bot import Message
from utils.bookingtime import *
from utils.sheetsconnect import *
from utils.keyaboard import main_keyboard
from utils.createdb import create_db

bot = Bot(os.environ["token"])
api = API(token=os.environ["token"])


class Branch(BaseStateGroup):
    HELLO = 0
    BOOKING = 1
    QUESTION = 2
    BOOKINGEND = 3


@bot.on.message(text="Начать")
async def start(m: Message) -> None:
    await m.answer("Выбери действие", keyboard=main_keyboard)
    await bot.state_dispenser.set(m.peer_id, Branch.HELLO)


@bot.on.message(state=Branch.HELLO, text="Бронь")
async def reg(m: Message) -> None:
    await m.answer(
        "Для посещения коворкинга необходимо пройти регистрацию.\n\nНо перед этим я познакомлю тебя с некоторыми правилами бронирования места:\n 1.Сеанс в коворкинге длится 2 часа\n 2.Нельзя забронировать новый сеанс, пока не истекло время текущего\n3. Забронировать место в коворкинге можно только в его рабочие часы: с 10 до 18\n\nЧтобы продолжить регистрацию, введи ФИО."
    )
    await bot.state_dispenser.set(m.peer_id, Branch.BOOKING)


@bot.on.message(state=Branch.BOOKING)
async def time(m: Message) -> None:
    btime = await timebuttons()
    if len(btime) == 0:
        await m.answer(
            "Команда коворкинга работает с 10 до 18 часов и готова ответить на все ваши вопросы только в эти часы. В остальное время мы отдыхаем и вам советуем💙",
            keyboard=main_keyboard,
        )
        await bot.state_dispenser.set(m.peer_id, Branch.HELLO, name=str(m.text))
    elif btime[0] == "Full":
        await m.answer(
            "Кажется у нас аншлаг🙊\n\nК сожалению, все места на ближайшие сеансы уже заняты. Возвращайся чуть позже и забирай свое место в SutSpace!",
            keyboard=main_keyboard,
        )
        await bot.state_dispenser.set(m.peer_id, Branch.HELLO, name=str(m.text))
    else:
        keyboard = Keyboard(one_time=True)
        for i in btime:
            keyboard.add(Text(i), color=KeyboardButtonColor.PRIMARY)
        await m.answer(
            "Отлично! Теперь выбери удобное время для сеанса:",
            keyboard=keyboard,
        )
        await bot.state_dispenser.set(m.peer_id, Branch.BOOKINGEND, name=str(m.text))


@bot.on.message(state=Branch.BOOKINGEND)
async def bookingComplete(m: Message):
    if await bookingCheck(m.text, m.peer_id):
        await m.answer("Ты уже зарегистрирован на это время", keyboard=main_keyboard)
        await bot.state_dispenser.set(m.peer_id, Branch.HELLO)
    else:
        await m.answer(
            "Ждем тебя в SutSpace!\n\nЗа 15 минут до окончания твоего сеанса я пришлю тебе напоминание💙",
            keyboard=main_keyboard,
        )
        await bookingDB(m.text, m.peer_id)
        await person_add(m.text, m.state_peer.payload["name"])
        await bot.state_dispenser.set(m.peer_id, Branch.HELLO)
        await notification(m.peer_id)


@bot.on.message(state=Branch.HELLO, text="Задать вопрос")
async def question(m: Message) -> None:
    await m.answer("Задай свой вопрос")
    await bot.state_dispenser.set(m.peer_id, Branch.QUESTION)


@bot.on.message(state=Branch.QUESTION)
async def questionComplete(m: Message):
    await m.answer(
        "Спасибо за обращение! Совсем скоро администратор коворкинга ответит тебе💙",
        keyboard=main_keyboard,
    )
    await bot.state_dispenser.set(m.peer_id, Branch.HELLO)


async def notification(peer):
    await sleep(6300)
    await api.messages.send(
        peer_id=peer,
        message="Пс, до окончания твоего сеанса осталось 15 минут...\nБыли рады видеть тебя в SutSpace, до новых встреч💙",
        random_id=0,
    )


if __name__ == "__main__":
    lw = LoopWrapper()
    lw.on_startup.append(create_db())
    lw.add_task(bot.run_polling())
    lw.run_forever()
