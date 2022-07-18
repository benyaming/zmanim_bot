from datetime import datetime as dt, date, timedelta
from typing import Tuple, Optional, Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.markdown import hbold, hitalic, hcode
from babel.support import LazyProxy

from zmanim_bot import texts
from zmanim_bot.exceptions import PolarCoordinatesException
from zmanim_bot.integrations.zmanim_models import Zmanim, Shabbat, RoshChodesh, DafYomi, Holiday, \
    IsraelHolidays, Fast, YomTov, AsurBeMelachaDay
from zmanim_bot.keyboards.inline import get_zmanim_by_date_buttons
from zmanim_bot.middlewares.i18n import gettext as _
from zmanim_bot.processors.text_utils import humanize_date, parse_jewish_date, humanize_time
from zmanim_bot.texts.plural import units
from zmanim_bot.texts.single import names, helpers, headers


def _emojize_holiday_title(holiday_type: str) -> str:
    emojis = {
        'chanukah': '🕎',
        'tu_bi_shvat': '🌳',
        'purim': '🎭',
        'lag_baomer': '🔥',
        'israel_holidays': '🇮🇱'
    }
    resp = f'{emojis[holiday_type]} {names.HOLIDAYS_TITLES[holiday_type]}'
    return resp


def _emojize_yom_tov_title(yom_tov_type: str) -> str:
    emojis = {
        'rosh_hashana': '🍯',
        'yom_kippur': '⚖️',
        'succot': '⛺️',
        'shmini_atzeres': '🏁',
        'pesach': '🍷',
        'shavuot': '🌾'
    }
    resp = f'{emojis[yom_tov_type]} {names.YOMTOVS_TITLES[yom_tov_type]}'
    return resp


def _compose_response(
        title: Union[LazyProxy, str],
        content: str,
        date_str: Optional[str] = None,
        location: Optional[str] = None
) -> str:
    title = hbold(title)
    location_str = f'📍 {hcode(location)}\n\n' if location else ''
    date_str = f'🗓 {date_str}\n' if date_str else ''
    if date_str and not location_str:
        date_str = f'{date_str}\n'
    resp = f'{title}\n\n' \
           f'{date_str}' \
           f'{location_str}' \
           f'{content}'
    return resp


def compose_zmanim(data: Zmanim, location_name: str) -> str:
    zmanim_rows: dict[str, dt] = data.dict(exclude={'settings', 'is_second_day'}, exclude_none=True)

    if len(zmanim_rows) == 0:
        raise PolarCoordinatesException()

    text_lines = []

    for zman_name, zman_value in zmanim_rows.items():
        header = hbold(getattr(texts.single.zmanim, zman_name) + ':')
        value = humanize_time(zman_value) if isinstance(zman_value, date) \
            else humanize_time(zman_value)
        line = f'{header} {value}'
        text_lines.append(line)

    content = '\n'.join(text_lines)

    date_str = hitalic(f'{humanize_date([data.settings.date_])} / '
                       f'{parse_jewish_date(data.settings.jewish_date)}')
    resp = _compose_response(f'🕓 {names.title_zmanim}', content, date_str, location_name)
    return resp


def compose_shabbat(data: Shabbat, location_name: str) -> Tuple[str, Optional[InlineKeyboardMarkup]]:
    torah_part = names.TORAH_PARTS.get(data.torah_part, '')
    date_str = hitalic(humanize_date([data.settings.date_]))
    torah_part_str = f'{hbold(headers.parsha + ":")} {torah_part}'

    if not data.candle_lighting:
        polar_error = hitalic('\n' + helpers.cl_error_warning)
        content = f'{torah_part_str}\n\n{polar_error}'
        resp = _compose_response(names.title_shabbath, content, date_str, location_name)
        return resp, None

    cl_str = f'{hbold(headers.cl + ":")} {humanize_time(data.candle_lighting)}'
    cl_offset = data.settings.cl_offset
    cl_offset_str = hitalic(f'({cl_offset} {_(*units.tu_minute, cl_offset)} {helpers.cl_offset})')

    havdala_str = f'{hbold(headers.havdala + ":")} {humanize_time(data.havdala)}'
    late_cl_warning = '\n\n' + hitalic(helpers.cl_late_warning) if data.late_cl_warning else ''

    content = f'{torah_part_str}\n' \
              f'{cl_str} {cl_offset_str}\n' \
              f'{havdala_str} {late_cl_warning}'
    resp = _compose_response(f'🕯 {names.title_shabbath}', content, date_str, location_name)

    kb = get_zmanim_by_date_buttons([data.havdala.date()])
    return resp, kb


def compose_rosh_chodesh(data: RoshChodesh) -> str:
    date_str = hitalic(humanize_date(data.days))

    month_str = f'{hbold(_(*units.tu_month, 1).capitalize() + ":")} {names.JEWISH_MONTHS[data.month_name]}'
    duration_str = f'{hbold(headers.rh_duration) + ":"} {data.duration}'
    molad = data.molad[0]
    molad_value = f'{molad.day} {names.MONTH_NAMES_GENETIVE[molad.month]} {molad.year},' \
                  f'{molad.time().hour} {_(*units.tu_hour, molad.time().hour)} ' \
                  f'{molad.time().minute} {_(*units.tu_minute, molad.time().minute)} ' \
                  f'{helpers.and_word} {data.molad[1]} {_(*units.tu_part, data.molad[1])}'
    molad_str = f'{hbold(headers.rh_molad) + ":"} {molad_value}'

    content = f'{month_str}\n' \
              f'{duration_str}\n' \
              f'{molad_str}'

    resp = _compose_response(f'🌙 {names.title_rosh_chodesh}', content, date_str)
    return resp


def compose_daf_yomi(data: DafYomi) -> str:
    date_str = hitalic(f'{humanize_date([data.settings.date_])}')

    masehet_str = f'{hbold(headers.daf_masehet) + ":"} {names.GEMARA_BOOKS.get(data.masehet, "")}'
    daf_str = f'{hbold(headers.daf_page) + ":"} {data.daf}'
    content = f'{masehet_str}\n{daf_str}'
    resp = _compose_response(f'📚 {names.title_daf_yomi}', content, date_str)
    return resp


def compose_holiday(data: Holiday) -> str:
    holiday_last_date = data.date
    if data.settings.holiday_name == 'chanukah':
        holiday_last_date += timedelta(days=7)

    date_value = humanize_date([data.date, holiday_last_date])
    date_str = f'{hbold(headers.date) + ":"} {date_value}'
    resp = _compose_response(_emojize_holiday_title(data.settings.holiday_name), date_str)
    return resp


def compose_israel_holidays(data: IsraelHolidays) -> str:
    content_lines = []
    for holiday in data.holiday_list:
        line = f'{hbold(headers.israel_holidays[holiday[0]]) + ":"} {humanize_date([holiday[1]])}'
        content_lines.append(line)

    content = '\n'.join(content_lines)
    resp = _compose_response(_emojize_holiday_title('israel_holidays'), content)
    return resp


def compose_fast(data: Fast, location_name: str) -> Tuple[str, InlineKeyboardMarkup]:
    deferred_fast_header = headers.fast_moved.value if data.moved_fast \
        else headers.fast_not_moved.value
    deferred_fast_str = hitalic(deferred_fast_header)

    fast_start_date = humanize_date([data.fast_start])
    fast_start_time = humanize_time(data.fast_start)
    fast_start_str = f'{hbold(headers.fast_start) + ":"} {fast_start_date}, {fast_start_time}'

    if data.chatzot:
        chatzot_time = humanize_time(data.chatzot)
        chatzot_str = f'\n{hbold(texts.single.zmanim.chatzos) + ":"} {chatzot_time}'
    else:
        chatzot_str = ''

    havdala_header = hbold(headers.fast_end)
    havdala_5_95_str = f'{hbold(headers.fast_end_5_95_dgr + ":")} ' \
                       f'{humanize_time(data.havdala_5_95_dgr)}'
    havdala_8_5_str = f'{hbold(headers.fast_end_8_5_dgr + ":")} ' \
                       f'{humanize_time(data.havdala_8_5_dgr)}'
    havdala_42_str = f'{hbold(headers.fast_end_42_min + ":")} ' \
                       f'{humanize_time(data.havdala_42_min)}'

    content = f'{fast_start_str}\n' \
              f'{deferred_fast_str}\n' \
              f'{chatzot_str}\n' \
              f'{havdala_header}\n' \
              f'{havdala_5_95_str}\n' \
              f'{havdala_8_5_str}\n' \
              f'{havdala_42_str}'

    resp = _compose_response(
        names.FASTS_TITLES[data.settings.fast_name],
        content,
        location=location_name
    )
    kb = get_zmanim_by_date_buttons([data.havdala_42_min.date()])
    return resp, kb


def compose_yom_tov(data: YomTov, location_name: str) -> Tuple[str, InlineKeyboardMarkup]:
    dates = [
        data.pre_shabbat,
        data.pesach_eating_chanetz_till and (
            data.pesach_eating_chanetz_till,
            data.pesach_burning_chanetz_till
        ),
        data.day_1,
        data.day_2,
        data.post_shabbat,
        data.pesach_part_2_day_1,
        data.pesach_part_2_day_2,
        data.pesach_part_2_post_shabat,
        data.hoshana_rabba
    ]
    dates = [d for d in dates if d is not None]

    lines = []

    yomtov_last_day = data.pesach_part_2_day_2 or data.pesach_part_2_day_1 \
                      or data.day_2 or data.day_1
    date_str = hitalic(humanize_date([data.day_1.date, yomtov_last_day.date]))

    for date_ in dates:
        if isinstance(date_, tuple) and isinstance(date_[0], dt):  # for pesach chametz times
            header = hbold(headers.pesach_end_eating_chametz + ':')
            value = humanize_time(date_[0])
            lines.append(f'{header} {value}')

            header = hbold(headers.pesach_end_burning_chametz + ':')
            value = humanize_time(date_[1])
            lines.append(f'{header} {value}\n')
            continue
        if isinstance(date_, date):  # hoshana rabbah case
            header = hbold(headers.hoshana_raba + ':')
            value = f'{date_.day} {names.MONTH_NAMES_GENETIVE[date_.month]}, ' \
                    f'{names.WEEKDAYS[date_.weekday()]}'
            lines.append(f'{header} {value}\n')
            continue
        if date_ == data.pesach_part_2_day_1:
            lines.append('\n')
        if date_.candle_lighting:

            if date_.candle_lighting.weekday() == 4:
                shabbat = f' ({names.shabbat})'
            else:
                shabbat = ''

            header = f'{headers.cl} {date_.candle_lighting.day} ' \
                     f'{names.MONTH_NAMES_GENETIVE[date_.candle_lighting.month]}{shabbat}'
            lines.append(f'{hbold(header + ":")} {humanize_time(date_.candle_lighting)}')

        if date_.havdala:
            header = f'{headers.havdala} {date_.havdala.day} ' \
                     f'{names.MONTH_NAMES_GENETIVE[date_.havdala.month]}'
            lines.append(f'{hbold(header + ":")} {humanize_time(date_.havdala)}')

    content = '\n'.join(lines)
    resp = _compose_response(
        _emojize_yom_tov_title(data.settings.yomtov_name),
        content,
        date_str,
        location_name
    )
    kb = get_zmanim_by_date_buttons(
        list(map(
            lambda d: d.date if isinstance(d, AsurBeMelachaDay) else d,
            filter(lambda v: isinstance(v, AsurBeMelachaDay), dates)
        ))
    )
    return resp, kb
