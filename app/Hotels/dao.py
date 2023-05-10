from app.bookings.models import Bookings
from app.DAO.base import BaseDAO
from app.database import async_session_maker, engine
from app.Hotels.models import Hotels
from sqlalchemy import select, and_, func
from datetime import date

from app.Hotels.rooms.models import Rooms


class HotelDAO(BaseDAO):
	model = Hotels

	@classmethod
	async def find_all_by_location(cls, location: str, date_from: date, date_to: date):
		"""
				with booked_hotel_rooms as
				(select * from public.booking as b
				left join public.room as r on b.room_id = r.id
				where
				b.date_to >= '2023-06-20' and
				b.date_from <= '2023-07-05')

				select h.name, h.location, h.room_quantity - count(bhr.hotel_id) from public.hotel as h
				left join booked_hotel_rooms as bhr on bhr.hotel_id = h.id
				where h.location like '%Алтай%'
				group by h.name, h.location, h.room_quantity, bhr.hotel_id;
		"""

		booked_hotel_rooms = select(Bookings, Rooms).select_from(Bookings).\
								join(Rooms, Bookings.room_id == Rooms.id, isouter=True).\
								where(and_(Bookings.date_to >= date_from),
									and_(Bookings.date_from <= date_to)).cte("booked_hotel_rooms")

		get_hotels_with_remaining_rooms = select(Hotels.id,
												 Hotels.name,
												 Hotels.location,
												 Hotels.services,
												 Hotels.rooms_quantity,
												 Hotels.image_id,
												 ((Hotels.rooms_quantity - func.count(booked_hotel_rooms.c.hotel_id)).label("rooms_left"))
												 ).select_from(Hotels).join(
												booked_hotel_rooms, Hotels.id == booked_hotel_rooms.c.hotel_id, isouter=True
												).filter(cls.model.location.like(f'%{location}%')
												).having((Hotels.rooms_quantity - func.count(booked_hotel_rooms.c.hotel_id)) > 0
												).group_by(Hotels.id, Hotels.name, Hotels.location, Hotels.rooms_quantity, booked_hotel_rooms.c.hotel_id)
		print(get_hotels_with_remaining_rooms.compile(engine , compile_kwargs = {'literal_binds':True} ))
		async with async_session_maker() as session:
			result = await session.execute(get_hotels_with_remaining_rooms)
			return result.all()
