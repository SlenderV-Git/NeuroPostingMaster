import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from aiogram import Bot, Dispatcher, types
from app.bot.filter import IsUser
from aiogram.filters import Command
from aiogram.types import Message

from app.core.settings import get_settings
from app.userbot.user_core import collect_post, send_message


POST_MESSAGE = []

bot = Bot(token=get_settings().env.bot_token)

dp = Dispatcher()

scheduler = AsyncIOScheduler()
daily_job = None
interval_job = None

async def send_post_to_bot():
    global POST_MESSAGE
    if POST_MESSAGE:
        print("Отправляю сообщение")
        bot_data = await bot.get_me()
        message = POST_MESSAGE.pop()
        await send_message(app=get_settings().app.get_client,
                           chat_id=bot_data.username,
                           message=message,
                           gpt=get_settings().gpt.get_gpt,
                           prompt=get_settings().env.prompt)
    else:
        print("Сообщений для отправки нет")

async def collect_posts():
    global POST_MESSAGE
    POST_MESSAGE = await collect_post(app=get_settings().app.get_client, 
                                      limit=10, 
                                      chats=get_settings().env.chats_input)
    print(f"Собрано {len(POST_MESSAGE)} постов")
    
async def schedule_daily_post(hour: int, minute: int):
    global daily_job
    if daily_job:
        daily_job.remove()
    trigger = CronTrigger(hour=hour, minute=minute)
    daily_job = scheduler.add_job(collect_posts, trigger)

async def schedule_interval_posts(hour: int, minute: int):
    global interval_job
    if interval_job:
        interval_job.remove()
    trigger = IntervalTrigger(hours=hour, minutes=minute)
    interval_job = scheduler.add_job(send_post_to_bot, trigger)

@dp.message()
async def send_answer(message: Message):
    chats = get_settings().env.chats_output
    for chat in chats:
        chat_info = await bot.get_chat(chat)
        print(f"Сообщение в чат {chat_info.full_name}")
        await message.copy_to(chat_id=chat_info.id)

@dp.message(Command('start'))
async def start_command(message: Message):
    await message.answer("Бот запущен!")

'''@dp.message(Command('settime'))
async def set_time_command(message: Message):
    try:
        time_str = message.text.split()[1]
        hour, minute = map(int, time_str.split(':'))
        schedule_daily_post(hour, minute)
        await message.answer(f"Посты будут отправляться ежедневно в {hour:02d}:{minute:02d}")
    except (IndexError, ValueError):
        await message.answer("Неверный формат. Используйте команду /settime HH:MM")'''

