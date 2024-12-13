from core.schemas.user import UserOut
from src.core.models import User
from tests.conftest import fake


def get_current_user(user: User) -> UserOut:
    return UserOut(
        username=user.username,
        email=user.email,
        disabled=user.disabled,
        superuser=user.superuser,
        id=user.id,
        uuid=user.uuid,
    )


def oauth2_scheme() -> str:
    token = fake.sha256()
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token
