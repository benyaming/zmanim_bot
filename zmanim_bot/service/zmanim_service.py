from io import BytesIO
from typing import Tuple, Optional

from aiogram.types import InlineKeyboardMarkup

from zmanim_bot.repository import bot_repository
from zmanim_bot.integrations import zmanim_api_client
from zmanim_bot.helpers import CallbackPrefixes
from zmanim_bot.states import ZmanimGregorianDateState
from zmanim_bot.processors.image import image_processor as ip


async def get_zmanim() -> BytesIO:
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_zmanim(
        user.get_active_location(),
        user.zmanim_settings.dict()
    )

    return ip.ZmanimImage(data).get_image()


async def get_zmanim_by_date(*, date: str = None, call_data: str = None) -> BytesIO:
    if call_data:
        date = call_data.split(CallbackPrefixes.zmanim_by_date)[1]

    user = await bot_repository.get_or_create_user()

    data = await zmanim_api_client.get_zmanim(
        user.get_active_location(),
        user.zmanim_settings.dict(),
        date_=date
    )

    return ip.ZmanimImage(data).get_image()


async def init_zmanim_by_date():
    await ZmanimGregorianDateState().waiting_for_gregorian_date.set()


async def get_shabbat() -> Tuple[BytesIO, Optional[InlineKeyboardMarkup]]:
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_shabbat(
        location=user.get_active_location(),
        cl_offset=user.cl_offset,
        havdala_opinion=user.havdala_opinion
    )

    return ip.ShabbatImage(data).get_image()


async def get_daf_yomi() -> BytesIO:
    data = await zmanim_api_client.get_daf_yomi()
    return ip.DafYomImage(data).get_image()


async def get_rosh_chodesh() -> BytesIO:
    data = await zmanim_api_client.get_rosh_chodesh()
    return ip.RoshChodeshImage(data).get_image()
