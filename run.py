import asyncio
from aiogram import Bot, Dispatcher
from app.database import database_init
from app.handlers import register_handlers
from dotenv import load_dotenv
import os
import logging

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def main():
    database_init()
    register_handlers(dp, bot)
    await dp.start_polling(bot)
    await bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
