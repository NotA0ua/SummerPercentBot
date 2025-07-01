from aiogram import Bot

from datetime import datetime, timezone, timedelta

from app.database import Database, UsersOperations

moscow_tz = timezone(timedelta(hours=3), name="MSK")

def get_summer_percents() -> float:
    now = datetime.now(moscow_tz)
    summer_start = datetime(2025, 6, 1, 0, 0, 0, tzinfo=moscow_tz)
    summer_end = datetime(2025, 9, 1, 0, 0, 0, tzinfo=moscow_tz)
    summer = summer_end - summer_start
    difference = now - summer_start
    percents = difference.total_seconds() / (summer.total_seconds() / 100)
    return percents


def summer_progress(percents: float, width: int, filled: str, empty: str):
    done = round((width * percents) / 100)
    rest = width - done

    return filled * done + empty * rest + f" {percents: 2.0f}%"


async def send_daily_message(bot: Bot, db: Database) -> None:
    percents = get_summer_percents()
    progress = summer_progress(percents, width=10, filled="🟥", empty="⬜")
    async with db.get_session() as session:
        users = await UsersOperations(session, 0).get_all_toggled_users()
        for user in users:
            await bot.send_message(user.id, f"Progress of your summer.\n{progress}")
