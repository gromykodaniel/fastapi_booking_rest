from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import select
from starlette.requests import Request
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings
from app.bookings.schemas import SBooking
from app.database import async_session_maker
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmatoon_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from fastapi_versioning import VersionedFastAPI, version

router  = APIRouter(
    prefix='/bookings',
    tags= ['Бронирование'],
)





@router.get('')
@version(1)
async def get_bookings(user : Users = Depends(get_current_user) ) -> list[SBooking]:
    return await BookingDAO.find_all(user_id = user.id)


@router.post('')
@version(1)
async def add_booking(
        room_id : int ,
        date_from : date ,
        date_to : date ,
        user : Users = Depends(get_current_user)
):

    booking = await BookingDAO.add(user.id , room_id , date_from ,date_to)
    booking_dict = parse_obj_as(SBooking , booking).dict()
    send_booking_confirmatoon_email.delay(booking_dict , user.email)
    return booking_dict


@router.delete('')
async def delete(user : Users = Depends(get_current_user) ) :
    return await BookingDAO.delete(user_id = user.id)
# @router.post('')
# async def add_booking(
#         room_id: int , date_from : date , date_to : date  ,
#         user : Users = Depends(get_current_user)
# ):
#
#     await BookingDAO.add(user.id , room_id , date_from, date_to,)
# если метод, где получать более одной записи ,
# то возвращаем список через ->[SBooking] (find_all)


# async def get_bookings(request:Request) -> SBooking:
    # return await BookingDAO.find_by_id(1)

