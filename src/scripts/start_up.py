import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.utils.utils import get_password_hash
from core.settings import settings
from core.db.db_helper import db_helper
from core.constants import ROOT_PATH


async def create_first_superuser(session: AsyncSession):
    USERNAME = settings.admin.username
    PASSWORD = get_password_hash(settings.admin.password)
    EMAIL = settings.admin.email

    stmt = select(User).filter(User.username == USERNAME)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        admin_user = User(
            username=USERNAME,
            password=PASSWORD,
            email=EMAIL,
            disabled=False,
            superuser=True,
        )
        session.add(admin_user)
        await session.commit()


async def prepare_folders():
    ROOT_PATH.mkdir(parents=True, exist_ok=True)


async def main():
    async with db_helper.session_factory() as session:
        await create_first_superuser(session)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
