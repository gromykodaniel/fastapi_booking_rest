import asyncio


from fastapi import APIRouter, Query
from starlette.responses import Response

from app.Hotels.dao import HotelDAO
from app.Hotels.rooms.dao import RoomDAO
from app.Hotels.rooms.schemas import SRoom, SRoomPrice
from app.Hotels.schemas import SHotel
from datetime import date, datetime
from pydantic import parse_obj_as, Field

from fastapi_cache.decorator import cache



router = APIRouter(
	prefix="/hotels",
	tags=["Отели"]
)


@router.get("/")
async def get_hotels():
	return await HotelDAO.find_all()


@router.get("/{location}")
@cache(expire=70)
async def get_hotels_by_location(location:  str ,
								date_from: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}"),
								date_to: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}")) :

	hotels =  await HotelDAO.find_all_by_location(location, date_from, date_to)
	hotels_json = parse_obj_as(list[SHotel] , hotels)
	return hotels_json





@router.get("/id/{hotel_id}")
async def get_hotels_by_id(hotel_id: int):
	return await HotelDAO.find_one_or_none( id = int(hotel_id) )



