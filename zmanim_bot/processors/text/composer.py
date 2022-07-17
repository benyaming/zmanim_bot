from datetime import datetime as dt, date
from typing import Tuple, Optional

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hitalic, hcode
from babel.support import LazyProxy

from zmanim_bot import texts
from zmanim_bot.exceptions import PolarCoordinatesException
from zmanim_bot.integrations.zmanim_models import Zmanim, Shabbat
from zmanim_bot.keyboards.inline import get_zmanim_by_date_buttons
from zmanim_bot.middlewares.i18n import gettext as _
from zmanim_bot.processors.text_utils import humanize_date, parse_jewish_date
from zmanim_bot.texts.plural import units
from zmanim_bot.texts.single import names, helpers, headers


def _compose_response(title: LazyProxy, date_str: str, location: str, content: str) -> str:
    title = hbold(title)
    location_str = hcode(location)
    resp = f'{title}\n\n' \
           f'🗓 {date_str}\n' \
           f'📍 {location_str}\n\n' \
           f'{content}'
    return resp


def compose_zmanim(data: Zmanim, location_name: str) -> str:
    zmanim_rows: dict[str, dt] = data.dict(exclude={'settings', 'is_second_day'}, exclude_none=True)

    if len(zmanim_rows) == 0:
        raise PolarCoordinatesException()

    text_lines = []

    for zman_name, zman_value in zmanim_rows.items():
        header = hbold(getattr(texts.single.zmanim, zman_name) + ':')
        value = zman_value.time().isoformat('minutes') if isinstance(zman_value, date) else \
            zman_value.isoformat('minutes')
        line = f'{header} {value}'
        text_lines.append(line)

    content = '\n'.join(text_lines)

    date_str = hitalic(f'{humanize_date([data.settings.date_])} / '
                       f'{parse_jewish_date(data.settings.jewish_date)}')
    resp = _compose_response(names.title_zmanim, date_str, location_name, content)
    return resp


def compose_shabbat(data: Shabbat, location_name: str) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    torah_part = names.TORAH_PARTS.get(data.torah_part, '')
    date_str = hitalic(f'{humanize_date([data.settings.date_])}')
    torah_part_str = f'{hbold(headers.parsha + ":")} {torah_part}'

    if not data.candle_lighting:
        polar_error = hitalic('\n' + helpers.cl_error_warning)
        content = f'{torah_part_str}\n\n{polar_error}'
        resp = _compose_response(names.title_shabbath, date_str, location_name, content)
        return resp, None

    cl_str = f'{hbold(headers.cl + ":")} {data.candle_lighting.time().isoformat("minutes")}'
    cl_offset = data.settings.cl_offset
    cl_offset_str = hitalic(f'({cl_offset} {_(*units.tu_minute, cl_offset)} {helpers.cl_offset})')

    havdala_str = f'{hbold(headers.havdala + ":")} {data.havdala.time().isoformat("minutes")}'
    late_cl_warning = '\n\n' + hitalic(helpers.cl_late_warning) if data.late_cl_warning else ''

    content = f'{torah_part_str}\n' \
              f'{cl_str} {cl_offset_str}\n' \
              f'{havdala_str} {late_cl_warning}'
    resp = _compose_response(names.title_shabbath, date_str, location_name, content)

    kb = get_zmanim_by_date_buttons([data.havdala.date()])
    return resp, kb
