from io import BytesIO
from typing import Tuple

from aiogram.types import InlineKeyboardMarkup

from zmanim_bot.integrations import zmanim_api_client
from zmanim_bot.processors.image.image_processor import (FastImage,
                                                         HolidayImage,
                                                         IsraelHolidaysImage,
                                                         YomTovImage)
from zmanim_bot.repository import bot_repository
from zmanim_bot.texts.single import buttons


def _get_festival_name(input_str: str) -> str:
    festival_shortcuts = {
        buttons.hom_rosh_hashana.value: 'rosh_hashana',
        buttons.hom_yom_kippur.value: 'yom_kippur',
        buttons.hom_succot.value: 'succot',
        buttons.hom_shmini_atzeret.value: 'shmini_atzeres',
        buttons.hom_chanukah.value: 'chanukah',
        buttons.hom_purim.value: 'purim',
        buttons.hom_pesach.value: 'pesach',
        buttons.hom_shavuot.value: 'shavuot',
        buttons.hom_tu_bishvat.value: 'tu_bi_shvat',
        buttons.hom_lag_baomer.value: 'lag_baomer',
        buttons.fm_gedaliah.value: 'fast_gedalia',
        buttons.fm_tevet.value: 'fast_10_teves',
        buttons.fm_esther.value: 'fast_esther',
        buttons.fm_tammuz.value: 'fast_17_tammuz',
        buttons.fm_av.value: 'fast_9_av',
    }
    return festival_shortcuts[input_str]


async def get_generic_fast(fast_name: str) -> Tuple[BytesIO, InlineKeyboardMarkup]:
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_generic_fast(
        name=_get_festival_name(fast_name),
        location=user.location.coordinates,
        havdala_opinion=user.havdala_opinion
    )
    return FastImage(data, user.location.name).get_image()


async def get_generic_yomtov(yomtov_name: str) -> Tuple[BytesIO, InlineKeyboardMarkup]:
    user = await bot_repository.get_or_create_user()
    data = await zmanim_api_client.get_generic_yomtov(
        name=_get_festival_name(yomtov_name),
        location=user.location.coordinates,
        cl_offset=user.cl_offset,
        havdala_opinion=user.havdala_opinion
    )
    return YomTovImage(data, user.location.name).get_image()


async def get_generic_holiday(holiday_name: str) -> BytesIO:
    if holiday_name == buttons.hom_israel:
        data = await zmanim_api_client.get_israel_holidays()
        return IsraelHolidaysImage(data).get_image()
    else:
        data = await zmanim_api_client.get_generic_holiday(_get_festival_name(holiday_name))
        return HolidayImage(data).get_image()
