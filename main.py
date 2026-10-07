import aiosqlite
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from os import getenv
from aiogram.client.session.aiohttp import AiohttpSession
from handlers.basic import router


load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)


async def main():

    bot = Bot(token=TOKEN)
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
