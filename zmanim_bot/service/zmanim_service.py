from io import BytesIO
from typing import Tuple, Optional

from aiogram.types import InlineKeyboardMarkup

from zmanim_bot.api import storage_api, zmanim_api
from zmanim_bot.states import ZmanimGregorianDateState
from zmanim_bot.processors.image import image_processor as ip


async def get_zmanim() -> BytesIO:
    user = await storage_api.get_or_create_user()
    data = await zmanim_api.get_zmanim(
        user.get_active_location(),
        user.zmanim_settings.dict()
    )

    return ip.ZmanimImage(data).get_image()


async def init_zmanim_by_date():
    await ZmanimGregorianDateState().waiting_for_gregorian_date.set()


async def get_shabbat() -> Tuple[BytesIO, Optional[InlineKeyboardMarkup]]:
    user = await storage_api.get_or_create_user()
    data = await zmanim_api.get_shabbat(
        location=user.get_active_location(),
        cl_offset=user.cl_offset,
        havdala_opinion=user.havdala_opinion
    )

    return ip.ShabbatImage(data).get_image()


async def get_daf_yomi() -> BytesIO:
    data = await zmanim_api.get_daf_yomi()
    return ip.DafYomImage(data).get_image()


async def get_rosh_chodesh() -> BytesIO:
    data = await zmanim_api.get_rosh_chodesh()
    return ip.RoshChodeshImage(data).get_image()


