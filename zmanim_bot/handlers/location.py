from asyncio import create_task

from aiogram.types import ContentType, Message

from ..misc import dp
from ..api import get_or_set_location
from ..helpers import LOCATION_PATTERN, parse_coordinates
from .redirects import redirect_to_main_menu


@dp.message_handler(regexp=LOCATION_PATTERN)
@dp.message_handler(content_types=[ContentType.LOCATION, ContentType.VENUE])
async def handle_location(msg: Message):
    if msg.location:
        lat = msg.location.latitude
        lng = msg.location.longitude
    else:
        lat, lng = parse_coordinates(msg.text)

    create_task(get_or_set_location((lat, lng)))
    return await redirect_to_main_menu()

