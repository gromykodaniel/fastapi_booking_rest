from fastapi import APIRouter, Query

from app.Hotels.rooms.schemas import SRoom
from app.Hotels.router import router
from app.Hotels.rooms.dao import RoomDAO
from datetime import date, datetime

router  = APIRouter(
    prefix='/rooms',
    tags= ['Комнаты в отелях'],
)


@router.get('/{hotel_id}/rooms', response_model=list[SRoom])
async def get_hotels_rooms(hotel_id: int ,
                           date_from: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}")
    , date_to: date = Query(..., description=f"Haпpuмep, {datetime.now().date()}" ) ) :
	return await RoomDAO.get_hotel_rooms(hotel_id , date_from , date_to)