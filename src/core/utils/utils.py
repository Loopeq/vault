from passlib.context import CryptContext
from core.enums.unit_time import UnitTime
from pathlib import Path

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def strip_error_msg(msg: str):
    return msg.split(":", 1)[-1].strip()


def get_freq(unit_time: UnitTime) -> str:
    freq_mapping = {
        'DAYS': 'D',
        'WEEKS': 'W',
        'MONTHS': 'M',
        'YEARS': 'Y'
    }
    return freq_mapping.get(unit_time.upper(), 'D')


def get_src_parent():
    current = Path(__file__).resolve()
    while current.parent.name != 'src':
        current = current.parent
    return current
