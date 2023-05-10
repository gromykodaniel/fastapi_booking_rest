from fastapi import APIRouter, Depends

from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.Hotels.router import get_hotels_by_location
from app.bookings.router import get_bookings
from app.users.router import read_users_me

router = APIRouter(
    prefix='/pages' ,
    tags=['Frontend']
)

templates = Jinja2Templates(directory='app/templates')

@router.get('/hotels')

async def get_hotels_page(
        request: Request,
        hotels = Depends(get_hotels_by_location)
):
    return templates.TemplateResponse(name='hotels.html' ,

                                      context={'request':request,
                                               'hotels':hotels}
                                      )


@router.get('')

async def get_main_page(
        request:Request ,

):
    return templates.TemplateResponse(name='main.html' , context={'request':request})

                                      # context={'request': request,
                                      #          'hotels': hotels}


@router.get('/me')
async def get_me_page(
        request : Request ,
        me = Depends(read_users_me),
        bookings = Depends(get_bookings)
):
    return templates.TemplateResponse(name = 'me.html' , context
    ={'request':request , 'me':me , 'bookings':bookings}

                                 )

