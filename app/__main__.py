from asyncio import run
import logging
from contextlib import suppress
from sys import stdout

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommand

from app import BOT_TOKEN
from app.database import Database
from app.handlers import setup_routers
from app.middlewares import DatabaseMiddleware, ThrottlingMiddleware

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

db = Database()
dp = Dispatcher()


async def on_startup() -> None:
    logging.basicConfig(level=logging.INFO, stream=stdout)

    await bot(DeleteWebhook(drop_pending_updates=True))

    await db.init_db()

    router = setup_routers()
    dp.include_routers(router)

    dp.update.outer_middleware(DatabaseMiddleware(db))

    dp.message.middleware(ThrottlingMiddleware())

    await bot.set_my_commands(
        [BotCommand(command="start", description="🔄 Restart a bot"),
         BotCommand(command="toggle", description="▶️ Toggle sending messages")],
        types.BotCommandScopeDefault(),
    )


async def on_shutdown() -> None:
    await db.dispose()


async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    with suppress(KeyboardInterrupt):
        run(main())
