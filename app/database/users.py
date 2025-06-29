import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Users


class UsersOperations:
    def __init__(self, session: AsyncSession, user_id: int):
        self.session = session
        self.user_id = user_id

    async def create_user(self) -> Users | None:
        user = Users(id=self.user_id)
        self.session.add(user)

        logging.info(f"User has been created ({self.user_id})")

        return user

    async def get_user(self) -> Users | None:
        result = await self.session.execute(select(Users).filter_by(id=self.user_id))
        return result.scalar_one_or_none()

    async def get_all_toggled_users(self) -> list[Users | None]:
        result = await self.session.execute(select(Users).filter_by(toggle=True))
        return list(result.scalars().all())

    async def update_toggle(self) -> Users | None:
        toggle = not self.get_user().toggle
        result = await self.session.execute(
            update(Users)
            .where(Users.id == self.user_id)
            .values(toggle=toggle)
            .returning(Users)
        )
        return result.scalar_one_or_none()
