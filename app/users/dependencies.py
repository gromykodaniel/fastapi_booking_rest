from datetime import date, datetime, timedelta

from fastapi import Depends
from starlette.requests import Request

from app.config import settings
from app.exceptions import TokenAbsentException, IncorrentTokenFormatException, UserIsNotPresentException, \
    TokenExpiredException

from jose import jwt , JWTError

from app.users.dao import UsersDAO


def get_token(request : Request):

    token = request.cookies.get('booking_access_token')
    if not token:

        raise TokenAbsentException

    return token


async def get_current_user(token : str  = Depends(get_token)):

    try:
        payload = jwt.decode(
            token , settings.secret_key , settings.algorutm
        )

    except JWTError:
        raise  IncorrentTokenFormatException

    expire : str = payload.get('exp')

    if (not expire) or (int(expire) < (datetime.utcnow().timestamp() )):

        raise TokenExpiredException

    user_id : str = payload.get('sub')

    if not user_id:
        raise UserIsNotPresentException

    user = await UsersDAO.find_one_or_none(id=int(user_id))

    if not user:
        raise UserIsNotPresentException


    return user