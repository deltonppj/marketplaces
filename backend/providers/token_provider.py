from pytz import timezone
from datetime import datetime, timedelta

from jose import jwt

from core.configs import settings


def _create_token(type_token: str, lifetime: timedelta, sub: str) -> str:
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=sp) + lifetime

    payload['type'] = type_token
    payload['exp'] = expire
    payload['iat'] = datetime.now(tz=sp)
    payload['sub'] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    """
    https://jwt.io
    """
    return _create_token(
        type_token='access_token',
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
