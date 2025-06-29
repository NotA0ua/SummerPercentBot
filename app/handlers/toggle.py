from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import UsersOperations

router = Router()

@router.message(Command("toggle"))
async def toggle_handler(message: types.Message, session: AsyncSession) -> None:
    user_operations = UsersOperations(session, message.from_user.id)

    user = await user_operations.update_toggle()

    toggle = user.toggle

    message_text = f"You've successfully turned *{'on' if toggle else 'off'}* the messages!"

    await message.reply(message_text)
