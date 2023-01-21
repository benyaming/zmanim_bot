import re

from aiogram.types import InlineKeyboardMarkup

from zmanim_bot.helpers import FeatureType
from zmanim_bot.keyboards import notifications as kb_set
from zmanim_bot.repository import bot_repository
from zmanim_bot.repository.models import Event, ZmanTrigger


def process_init_notification(feature_type: str) -> tuple[str, InlineKeyboardMarkup]:
    match feature_type:
        case FeatureType.zmanim:
            kb = kb_set.zmanim_notifications_kb
        case _:
            raise ValueError('Unsupported notification type!')  # todo better handle

    resp = 'select zman for notification'  # todo translate
    return resp, kb


def process_offset(user_inout: str) -> int:
    offset_pattern = r'^(\+|-)?(\d+)$'

    if re_match := re.match(offset_pattern, user_inout):
        offset = int(re_match.groups()[1])

        if re_match.groups()[0] == '-':
            offset *= -1
    else:
        raise ValueError

    return offset


async def create_notification(data: dict):
    user = await bot_repository.get_or_create_user()
    feature_type: str = data['feature']

    match feature_type:
        case FeatureType.zmanim:
            trigger = ZmanTrigger(
                zman_type=data['zman_type'],
                offset=data['offset']
            )
        case _:
            raise ValueError('Unsupported notification type!')  # todo better handle

    event = Event(
        owner_id=user.user_id,
        name=data['name'],
        message=data['message'],
        trigger=trigger
    )
    await bot_repository.create_event(event)


