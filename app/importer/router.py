import os

from fastapi import FastAPI , APIRouter , UploadFile

import  csv
import codecs

import json

from pydantic import json
from datetime import date
from sqlalchemy import insert

from app.Hotels.models import Hotels
from app.Hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from app.database import async_session_maker

router = APIRouter(
    prefix='/import',
    tags = ['Import csv']

)

@router.post('/hotels')
async def add_hotel_info(tablename : str , file :UploadFile ):

    csv_name = file.filename
    csv_path = 'app/importer/uploads/'
    file_path = os.path.join(csv_path, csv_name)
    with open(file_path, mode='wb+') as f:
        f.write(file.file.read())

    with open(file_path, mode='r', encoding='utf-8') as csvf:

        csvReader = csv.DictReader(csvf, delimiter=';' )

        if tablename =='hotels':
            for rows in csvReader:
                name =rows['name']
                location =rows['location']
                services =  rows['services']
                rooms_quantity  = int(rows['rooms_quantity'])
                image_id = int(rows['image_id'])


                async with async_session_maker() as session:
                    name : str = name
                    location : str = location
                    services : json = services
                    rooms_quantity : int = rooms_quantity

                    image_id : int  = image_id
                    add_booking = (insert(Hotels).values(
                        name = name ,
                        location = location ,
                        services = services,
                        rooms_quantity = rooms_quantity,
                        image_id = image_id


                    ).returning(Hotels))
                    new_booking = await session.execute(add_booking)
                    await session.commit()

        elif tablename == 'rooms':
            for rows in csvReader:
                hotel_id = int(rows['hotel_id'])
                name =rows['name']
                description =  rows['description']
                price  = int(rows['price'])
                services =  rows['services']
                quantity = int (rows['quantity'] )
                image_id = int(rows['image_id'])

                async with async_session_maker() as session:
                    hotel_id : int = hotel_id
                    name : str = name
                    description : str = description
                    price : int = price
                    services : json = services
                    quantity : int = quantity
                    image_id : int  = image_id
                    add_rooms = (insert(Rooms).values(
                        hotel_id= hotel_id,
                        name = name ,
                        description = description,
                        price = price ,
                        services =services ,
                        quantity = quantity,
                        image_id = image_id
                    ).returning(Rooms))
                    new_booking = await session.execute(add_rooms)
                    await session.commit()

