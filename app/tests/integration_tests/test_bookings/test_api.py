
import pytest
from httpx import AsyncClient

@pytest.mark.parametrize('room_id , date_from , date_to , status_code',[
    *[(4,'2030-05-01','2030-05-15',200)]*9,
(4,'2030-05-01','2030-05-15',409),
(4,'2030-05-01','2030-05-15',409),
] )
async def test_add_and_get_booking(
room_id , date_from , date_to , status_code ,
        authenticated_ac: AsyncClient):
    responce = await authenticated_ac.post('/bookings', params={
        'room_id' : room_id ,
        'date_from': date_from,
        'date_to':date_to,


    })

    assert responce.status_code == status_code