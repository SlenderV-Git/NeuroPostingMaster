from typing import List
import asyncio
from app.bot.handlers import dp, bot, schedule_interval_posts, schedule_daily_post, scheduler

async def start_scheduler():
    if not scheduler.running:
        scheduler.start()

async def main():
    data = await bot.get_me()
    print(data.full_name)
    await schedule_daily_post(hour=6, minute=0)
    await schedule_interval_posts(hour= 0, minute= 10)
    await start_scheduler()
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    if not asyncio.get_event_loop().is_running():
        asyncio.run(main())
    else:
        loop = asyncio.get_event_loop()
        loop.create_task(main())

