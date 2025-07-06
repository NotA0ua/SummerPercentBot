from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.database import UsersOperations
from app.utils.daily import percent_message

router = Router()


@router.message(Command("percent"))
async def start_handler(message: types.Message, session: AsyncSession) -> None:
    user = await UsersOperations(session, message.from_user.id).get_user()
    if user.toggle:
        await message.answer(percent_message())
    else:
        await message.answer(
            "⚠️ *You've turned off sending of the messages!*\nTurn it on using /toggle."
        )
