from aiogram import Router
from aiogram.filters import CommandStart

start_router = Router()


@start_router.message(CommandStart)
async def start_command(message):
    await message.answer(f"Привет, {message.from_user.first_name}!")
