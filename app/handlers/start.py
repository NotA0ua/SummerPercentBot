from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import UsersOperations

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message, session: AsyncSession) -> None:
    user_operations = UsersOperations(session, message.from_user.id)
    if user_operations.get_user():
        await user_operations.create_user()
    await message.answer("Hello, this is a bot that shows you how much % of the *summer you've wasted*.\n It will send you a message every day at 00:00.")
