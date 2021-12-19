import json
from typing import Union

from aiogram import types

from zmanim_bot.repository.bot_repository import get_or_set_location
from ..config import REPORT_ADMIN_LIST
from ..exceptions import NoLocationException
from ..helpers import CallbackPrefixes
from ..misc import bot


async def _compose_report_text(report: dict) -> str:
    try:
        location = await get_or_set_location()
    except NoLocationException:
        location = None

    report_data = {
        'text': report['message'],
        'meta': {
            'user_id': types.User.get_current().id,
            'user_location': location
        }
    }
    report_text = json.dumps(report_data, indent=2, ensure_ascii=False)
    text = f'<b>NEW REPORT!</b>\n\n<code>{report_text}</code>'
    return text


async def _compose_media(report: dict) -> Union[types.MediaGroup, types.InputMediaPhoto]:
    media_ids = report['media_ids']

    media_photos = []
    for file_id, file_type in media_ids:
        media_types = {
            'photo': types.InputMediaPhoto,
            'video': types.InputMediaVideo
        }
        file = await bot.get_file(file_id)
        url = bot.get_file_url(file.file_path)
        media_photos.append(media_types[file_type](types.InputFile.from_url(url)))

    if len(media_photos) == 1:
        return media_photos[0]
    return types.MediaGroup(media_photos)


async def send_report_to_admins(report: dict):
    button_data = f'{CallbackPrefixes.report}{report["message_id"]}:{report["user_id"]}'
    button = types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('Reply to report', callback_data=button_data)
    )
    report_text = await _compose_report_text(report)
    report_media = await _compose_media(report) if report['media_ids'] else None

    for admin_id in REPORT_ADMIN_LIST:
        if report_media:
            if isinstance(report_media, types.MediaGroup):
                msg = await bot.send_media_group(admin_id, report_media)
            else:
                msg = await bot.send_photo(admin_id, report_media.file)

            resp_id = msg[0].message_id if isinstance(msg, list) else msg.message_id
            await bot.send_message(admin_id, report_text, reply_markup=button, reply_to_message_id=resp_id)
        else:
            await bot.send_message(admin_id, report_text, reply_markup=button)


async def send_response_to_user(response: dict):
    response_text = response['response']
    response_media = await _compose_media(response) if response['media_ids'] else None

    msg = await bot.send_message(
        response['user_id'],
        response_text,
        reply_to_message_id=response['message_id']
    )
    if response_media:
        if isinstance(response_media, types.MediaGroup):
            await bot.send_media_group(response['user_id'], response_media, reply_to_message_id=msg.message_id)
        else:
            await bot.send_photo(response['user_id'], response_media.file, reply_to_message_id=msg.message_id)
