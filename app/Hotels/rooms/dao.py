from app.bookings.models import Bookings
from app.DAO.base import BaseDAO
from app.database import async_session_maker
from app.Hotels.rooms.models import Rooms
from sqlalchemy import select, and_, func, or_
from datetime import date
from app.database import engine


class RoomDAO(BaseDAO):
	model = Rooms

	@classmethod
	async def get_hotel_rooms(cls, hotel_id: int,
							  date_from: date, date_to: date):


		total_days: int = (date_to - date_from).days



		hotel_rooms = select(Rooms.id,
							Rooms.hotel_id,
							Rooms.name,
							Rooms.description,
							Rooms.services,
							Rooms.price,
							Rooms.quantity,
							Rooms.image_id,
							(total_days * Rooms.price).label('total_price'),
							(Rooms.quantity - func.count(Bookings.id)).label("rooms_left")
							).join(Bookings, Bookings.room_id == Rooms.id, isouter=True).\
								where(
									and_(Rooms.hotel_id == hotel_id,
									or_(
										and_(
											Bookings.date_from <= date_to,
											Bookings.date_to >= date_from
										),
									  	and_(
											Bookings.date_to == None,
											Bookings.date_from == None
										)
									)
								)
							).group_by(Rooms.id)

		# print(hotel_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

		async with async_session_maker() as session:
			result = await session.execute(hotel_rooms)
			return result.all()