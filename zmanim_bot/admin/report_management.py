import json
from typing import Union

from aiogram import types
from aiogram.types import InputMediaPhoto

from ..config import REPORT_ADMIN_LIST
from ..misc import bot


async def compose_report(report: dict) -> Union[types.MediaGroup, str]:
    screenshots_ids = report.pop('screenshots_ids')
    report_text = json.dumps(report, indent=2, ensure_ascii=False)
    text = f'<b>NEW REPORT!</b>\n\n<code>{report_text}</code>'

    if not screenshots_ids:
        return text

    media_photos = []
    for file_id in screenshots_ids:
        file = await bot.get_file(file_id)
        url = bot.get_file_url(file.file_path)
        media_photos.append(InputMediaPhoto(types.InputFile.from_url(url)))

    media_photos[0].caption = text
    return types.MediaGroup(media_photos)


async def send_report_to_admins(report: dict):
    composed_report = await compose_report(report)

    for admin_id in REPORT_ADMIN_LIST:
        if isinstance(composed_report, types.MediaGroup):
            await bot.send_media_group(admin_id, composed_report)
        elif isinstance(composed_report, str):
            await bot.send_message(admin_id, composed_report)
