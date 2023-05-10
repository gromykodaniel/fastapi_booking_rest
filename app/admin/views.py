from sqladmin import ModelView

from app.Hotels.models import Hotels
from app.Hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]+ [Users.booking]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = 'fa-solid fa-user'


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c ]  + [Bookings.user , Bookings.room]
    # column_details_exclude_list = [Users.hashed_password]

    name = 'Бронь'
    name_plural = 'Брони'
    icon = 'fa-solid fa-book'

class HotelsAdmin(ModelView ,  model = Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [ Hotels.rooms]

    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'

class RoomAdmin(ModelView , model = Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel , Rooms.booking]

    name = ' Забронированный номер '
    name_plural = ' Забронированныe номерa '
    icon = 'fa-solid fa-bed'

