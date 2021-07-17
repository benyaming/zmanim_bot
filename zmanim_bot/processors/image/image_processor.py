from datetime import date
from datetime import datetime as dt
from datetime import timedelta
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from aiogram.types import InlineKeyboardMarkup
from babel.support import LazyProxy

from zmanim_bot import texts
from zmanim_bot.exceptions import PolarCoordinatesException
from zmanim_bot.helpers import parse_jewish_date
from zmanim_bot.integrations.zmanim_models import *
from zmanim_bot.keyboards.inline import get_zmanim_by_date_buttons
from zmanim_bot.middlewares.i18n import gettext as _
from zmanim_bot.processors.text_utils import humanize_date, humanize_time
from zmanim_bot.texts.plural import units
from zmanim_bot.texts.single import headers, helpers, names, zmanim

IMG_SIZE = 1181
Line = Tuple[Optional[str], Optional[str], Optional[bool]]
EMPTY_LINE = None, None, None


def _convert_img_to_bytes_io(img: PngImagePlugin.PngImageFile) -> BytesIO:
    bytes_io = BytesIO()
    img.save(bytes_io, 'png')
    bytes_io.seek(0)
    return bytes_io


def _get_draw(background_path: str) -> ImageDraw:
    image = Image.open(background_path)
    draw = ImageDraw.Draw(image)
    return image, draw


class BaseImage:
    _font_path = Path(__file__).parent / 'res' / 'fonts' / 'gothic.TTF'
    _bold_font_path = Path(__file__).parent / 'res' / 'fonts' / 'gothic-bold.TTF'
    _title_font = ImageFont.truetype(str(_bold_font_path), 60)
    _font_size = 0
    _warning_font_size = 0
    _background_path = None

    _image: PngImagePlugin.PngImageFile
    _draw: ImageDraw

    def __init__(self):
        self._font = ImageFont.truetype(str(self._font_path), self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), self._font_size)

        if self._background_path:
            self._image, self._draw = _get_draw(str(self._background_path))

        self._warning_font = ImageFont.truetype(str(self._bold_font_path), self._warning_font_size)

    def _draw_title(self, draw: ImageDraw, title: LazyProxy) -> None:
        coordinates = (180, 30)
        font = self._title_font
        draw.text(coordinates, title.value, font=font)

    def _draw_date(
            self,
            greg_date: List[Union[date, dt]],
            jewish_date: Optional[str] = None,
            no_weekday: bool = False
    ):
        x = 180
        y = 100

        greg_date_str = humanize_date(greg_date)
        if no_weekday:
            greg_date_str = greg_date_str.split(', ')[0]

        jewish_date_str = f' / {parse_jewish_date(jewish_date)}' if jewish_date else ''
        date_str = f'{greg_date_str}{jewish_date_str}'

        date_font = ImageFont.truetype(str(self._font_path), 40)
        self._draw.text((x, y), date_str, font=date_font)

    def _draw_location(self, location_name: str, *, is_fast: bool = False):
        x = 185
        y = 150 if not is_fast else 100

        icon_font = ImageFont.truetype(str(Path(__file__).parent / 'res' / 'fonts' / 'fontello.ttf'), 40)
        text_font = ImageFont.truetype(str(self._font_path), 40)

        self._draw.text((x, y + 5), f'\ue800', font=icon_font, embedded_color=True)
        self._draw.text((x + 20, y), f' {location_name}', font=text_font, embedded_color=True)

    def _x_font_offset(self, text: str) -> int:
        """Returns size in px of given text in axys x"""
        last_line = text.split('\n')[-1]

        return self._bold_font.getsize(last_line)[0]

    def _y_font_offset(self, text: str) -> int:
        """Returns size in px of given text in axys y"""
        return self._bold_font.getsize(text)[1]

    def _draw_line(
            self,
            x: int,
            y: int,
            header: str,
            value: str,
            value_on_new_line: bool = False,
            value_without_x_offset: bool = False
    ):
        header = f'{str(header)}: '
        self._draw.text((x, y), text=header, font=self._bold_font)

        if not value_without_x_offset:
            x += self._x_font_offset(header)
        if value_on_new_line or value_without_x_offset:
            y += self._y_font_offset(header.split('\n')[0])

        self._draw.text((x, y), text=str(value), font=self._font)

    def get_image(self):
        raise NotImplemented


class DafYomImage(BaseImage):
    def __init__(self, data: DafYomi):
        self._font_size = 90
        self.data = data
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'daf_yomi.png'

        super().__init__()
        self._draw_title(self._draw, names.title_daf_yomi)
        self._draw_date([self.data.settings.date_], self.data.settings.jewish_date)

    def get_image(self) -> BytesIO:
        y = 470
        x = 100
        y_offset = 100

        # draw masehet
        self._draw_line(x, y, headers.daf_masehet, names.GEMARA_BOOKS.get(self.data.masehet, ''))
        y += y_offset

        # draw daf
        self._draw_line(x, y, headers.daf_page, str(self.data.daf))

        return _convert_img_to_bytes_io(self._image)


class RoshChodeshImage(BaseImage):
    def __init__(self, data: RoshChodesh):
        self.data = data
        self._font_size = 52
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'rosh_hodesh.png'

        super().__init__()
        self._draw_title(self._draw, names.title_rosh_chodesh)
        self._draw_date(self.data.days, self.data.settings.jewish_date)

    def get_image(self) -> BytesIO:
        y = 370
        x = 100
        y_offset = 80

        # draw month
        self._draw_line(x, y, _(*units.tu_month, 1).capitalize(),
                        names.JEWISH_MONTHS[self.data.month_name])
        y += y_offset

        # draw duration
        duration_value = f'{self.data.duration} {_(*units.tu_day, self.data.duration)}'
        self._draw_line(x, y, headers.rh_duration, duration_value)
        y += y_offset

        # # draw date
        # date_value = humanize_date(self.data.days, weekday_on_new_line=len(self.data.days) > 1)
        # self._draw_line(x, y, headers.date, date_value)
        # y += y_offset if len(self.data.days) == 1 else y_offset * 2

        # draw molad string
        molad = self.data.molad[0]
        molad_value = f'{molad.day} {names.MONTH_NAMES_GENETIVE[molad.month]} {molad.year},\n' \
                      f'{molad.time().hour} {_(*units.tu_hour, molad.time().hour)} ' \
                      f'{molad.time().minute} {_(*units.tu_minute, molad.time().minute)} ' \
                      f'{helpers.and_word} {self.data.molad[1]} {_(*units.tu_part, self.data.molad[1])}'
        self._draw_line(x, y, headers.rh_molad, molad_value)

        return _convert_img_to_bytes_io(self._image)


class ShabbatImage(BaseImage):

    def __init__(self, data: Shabbat, location_name: str):
        self.data = data
        self._font_size = 60
        self._warning_font_size = 48
        self.location_name = location_name

        super().__init__()

    def get_image(self) -> Tuple[BytesIO, Optional[InlineKeyboardMarkup]]:
        if not self.data.candle_lighting or self.data.late_cl_warning:
            self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'shabbos_attention.png'
        else:
            self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'shabbos.png'
        self._image, self._draw = _get_draw(str(self._background_path))

        self._draw_title(self._draw, names.title_shabbath)
        self._draw_location(self.location_name)

        if self.data.havdala:
            self._draw_date([self.data.havdala.date()], no_weekday=True)

        y = 400 if self.data.candle_lighting else 470
        x = 100
        y_offset: int = 80

        # draw parashat hashavua
        torah_part = names.TORAH_PARTS.get(self.data.torah_part, '')
        if (self._x_font_offset(headers.parsha.value) + self._x_font_offset(
                torah_part) + x) > IMG_SIZE:
            value_on_new_line = True
        else:
            value_on_new_line = False

        self._draw_line(x, y, headers.parsha, torah_part, value_without_x_offset=value_on_new_line)
        y += y_offset if not value_on_new_line else y_offset * 2

        # if polar error, draw error message and return
        if not self.data.candle_lighting:
            x = 100
            y = 840 if helpers.cl_error_warning.value.count('\n') < 2 else 810

            self._draw.text((x, y), helpers.cl_error_warning.value, font=self._warning_font,
                            fill='#ff5959')
            return _convert_img_to_bytes_io(self._image), None

        # draw candle lighting
        self._draw_line(x, y, headers.cl, self.data.candle_lighting.time().isoformat('minutes'))
        y += y_offset

        # draw shekiah offset
        cl_offset = self.data.settings.cl_offset
        offset_value = f'({cl_offset} {_(*units.tu_minute, cl_offset)} {helpers.cl_offset})'
        self._draw.text((x, y), offset_value, font=self._font)
        y += y_offset

        # draw havdala
        self._draw_line(x, y, headers.havdala, self.data.havdala.time().isoformat('minutes'))
        y += y_offset

        kb = get_zmanim_by_date_buttons([self.data.havdala.date()])

        # draw warning if need
        if not self.data.late_cl_warning:
            return _convert_img_to_bytes_io(self._image), kb

        x, y = 100, 840
        self._draw.text((x, y), helpers.cl_late_warning.value, font=self._warning_font,
                        fill='#ff5959')

        return _convert_img_to_bytes_io(self._image), kb


class ZmanimImage(BaseImage):

    def __init__(self, data: Zmanim, location_name: str):
        self.data = data
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'zmanim.png'
        super().__init__()

        self._draw_title(self._draw, names.title_zmanim)
        self._draw_date([self.data.settings.date_], self.data.settings.jewish_date)
        self._draw_location(location_name)

    def _set_font_properties(self, number_of_lines: int):
        p = {
            # [font_size, y_offset, start_y_offset
            1: [44, 53, 350],
            2: [44, 53, 300],
            3: [44, 53, 270],
            4: [44, 53, 220],
            5: [44, 53, 180],
            6: [44, 53, 160],
            7: [44, 53, 140],
            8: [44, 53, 100],
            9: [44, 53, 100],
            10: [44, 53, 80],
            11: [44, 53, 40],
            12: [44, 53, 25],
            13: [44, 53, 30],
            14: [44, 53, 30],
            15: [44, 53, 20],
            16: [40, 42, 20],
            17: [40, 42, 20],
            18: [40, 42, 0],
            19: [40, 42, 0]
        }
        self._font_size, self._y_offset, self._start_y_offset = p.get(number_of_lines)
        self._font = ImageFont.truetype(str(self._font_path), size=self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), size=self._font_size)

    def get_image(self) -> BytesIO:
        zmanim_rows: Dict[str, dt] = self.data.dict(exclude={'settings'}, exclude_none=True)

        if len(zmanim_rows) == 0:
            raise PolarCoordinatesException()

        self._set_font_properties(len(zmanim_rows))

        y: int = 200 + self._start_y_offset
        x: int = 50

        # draw all image lines in cycle
        for header, value in zmanim_rows.items():
            self._draw_line(
                x, y, getattr(texts.single.zmanim, header),
                value.time().isoformat('minutes') if isinstance(value, date) else value.isoformat(
                    'minutes')
            )
            y += self._y_offset

        return _convert_img_to_bytes_io(self._image)


class FastImage(BaseImage):

    def __init__(self, data: Fast, location_name: str):
        self.data = data
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'fast.png'
        self._font_size = 60

        super().__init__()

        self._draw_title(self._draw, names.FASTS_TITLES[data.settings.fast_name])
        self._draw_location(location_name, is_fast=True)

    def get_image(self) -> Tuple[BytesIO, InlineKeyboardMarkup]:

        self._draw.text(
            (210, 150),
            headers.fast_moved.value if self.data.moved_fast else headers.fast_not_moved.value,
            font=self._bold_font,
            fill='#ff5959' if self.data.moved_fast else '#8bff59'
        )

        x = 100
        y = 300 if self.data.chatzot else 350

        y_offset = 80

        # draw date and start time
        fast_date, fast_weekday = humanize_date([self.data.fast_start]).split(', ')
        fast_start_value = f'{fast_date},\n{fast_weekday}, {self.data.fast_start.time().isoformat("minutes")}'
        self._draw_line(x, y, headers.fast_start, fast_start_value)
        y += self._y_font_offset(fast_start_value) + y_offset + y_offset

        # draw hatzot, if need
        if self.data.chatzot:
            self._draw_line(x, y, zmanim.chatzos, self.data.chatzot.time().isoformat('minutes'))
            y += y_offset

        # draw havdala
        self._draw_line(x, y, headers.fast_end, '')
        y += y_offset
        havdala_options = (
            (self.data.havdala_5_95_dgr, headers.fast_end_5_95_dgr),
            (self.data.havdala_8_5_dgr, headers.fast_end_8_5_dgr),
            (self.data.havdala_42_min, headers.fast_end_42_min)
        )
        for havdala_value, havdala_header in havdala_options:
            self._draw_line(x, y, havdala_header, havdala_value.time().isoformat('minutes'))
            y += y_offset

        kb = get_zmanim_by_date_buttons([self.data.havdala_42_min.date()])
        return _convert_img_to_bytes_io(self._image), kb


class HolidayImage(BaseImage):

    def __init__(self, data: Holiday):
        self.data = data
        background_and_font_params = {
            'chanukah': ('chanuka.png', 60),
            'tu_bi_shvat': ('tubishvat.png', 70),
            'purim': ('purim.png', 70),
            'lag_baomer': ('lagbaomer.png', 70),
            'israel_holidays': ('israel_holidays.png', 50),
        }
        background, font_size = background_and_font_params[data.settings.holiday_name]

        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / background
        self._font_size = font_size

        super().__init__()

        self._draw_title(self._draw, names.HOLIDAYS_TITLES[data.settings.holiday_name])

    def get_image(self) -> BytesIO:
        x = 100
        y = 450

        holiday_last_date = self.data.date
        line_break = False
        if self.data.settings.holiday_name == 'chanukah':
            holiday_last_date += timedelta(days=7)
            line_break = True

        date_value = humanize_date([self.data.date, holiday_last_date],
                                   weekday_on_new_line=line_break)

        if (x + self._x_font_offset(headers.date.value) + self._x_font_offset(
                date_value)) > IMG_SIZE:
            date_value = humanize_date([self.data.date, holiday_last_date],
                                       weekday_on_new_line=True)

        self._draw_line(
            x,
            y,
            headers.date,
            date_value)
        return _convert_img_to_bytes_io(self._image)


class IsraelHolidaysImage(BaseImage):

    def __init__(self, data: IsraelHolidays):
        self.data = data
        self._background_path = Path(
            __file__).parent / 'res' / 'backgrounds' / 'israel_holidays.png'
        self._font_size = 53

        super().__init__()

        self._draw_title(self._draw, names.HOLIDAYS_TITLES['israel_holidays'])

    def get_image(self) -> BytesIO:
        x = 80
        y = 300
        y_offset = 90
        y_offset_small = 60

        for holiday in self.data.holiday_list:
            self._draw.text((x, y), f'{headers.israel_holidays[holiday[0]]}:',
                            font=self._bold_font)
            y += y_offset_small
            self._draw_line(x, y, headers.date, humanize_date([holiday[1]]))
            y += y_offset

        return _convert_img_to_bytes_io(self._image)


class YomTovImage(BaseImage):

    def __init__(self, data: YomTov, location_name: str):
        backgrounds = {
            'rosh_hashana': 'rosh_hashana.png',
            'yom_kippur': 'yom_kippur.png',
            'succot': 'succos.png',
            'shmini_atzeres': 'shmini_atzeret.png',
            'pesach': 'pesah.png',
            'shavuot': 'shavuot.png',
        }
        background = backgrounds[data.settings.yomtov_name]

        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / background

        super().__init__()

        self.data = data
        self._draw_title(self._draw, names.YOMTOVS_TITLES[data.settings.yomtov_name])
        self._draw_location(location_name)

    @staticmethod
    def _humanize_header_date(header_type: str, date_: Union[date, dt]) -> Tuple[str, bool]:
        """
        Use this function for date header, not for date title.
        :return header and flag indicates if it's two-lines height header
        """
        if header_type == headers.cl and date_.weekday() == 4:
            shabbat = f'\n({names.shabbat})'
        else:
            shabbat = ''

        resp = f'{header_type} {date_.day} {names.MONTH_NAMES_GENETIVE[date_.month]}{shabbat}'
        return resp, bool(shabbat)

    def _get_dates(self) -> List[Union[AsurBeMelachaDay, date]]:
        dates = [
            self.data.pre_shabbat,
            self.data.day_1,
            self.data.day_2,
            self.data.post_shabbat,
            self.data.pesach_part_2_day_1,
            self.data.pesach_part_2_day_2,
            self.data.hoshana_rabba
        ]
        return [d for d in dates if d is not None]

    def _prepare_lines(self, dates: List[Union[AsurBeMelachaDay, date]]) -> List[Line]:
        lines = []

        yomtov_last_day = self.data.pesach_part_2_day_2 \
                          or self.data.pesach_part_2_day_1 \
                          or self.data.day_2 \
                          or self.data.day_1
        self._draw_date([self.data.day_1.date, yomtov_last_day.date])
        # dates_range = humanize_date([self.data.day_1, yomtov_last_day], weekday_on_new_line=True)
        # lines.append((headers.date, dates_range, False))
        # lines.append(EMPTY_LINE)

        for date_ in dates:
            if isinstance(date_, date):  # hoshana rabbah case
                header = str(headers.hoshana_raba)
                value = f'{date_.day} {names.MONTH_NAMES_GENETIVE[date_.month]},\n {names.WEEKDAYS[date_.weekday()]}'
                lines.append(EMPTY_LINE)
                lines.append((header, value, False))
                continue

            if date_ == self.data.pesach_part_2_day_1:
                lines.append(EMPTY_LINE)

            if date_.candle_lighting:
                header, new_line = self._humanize_header_date(headers.cl, date_.candle_lighting)
                value = humanize_time(date_.candle_lighting.time())
                lines.append((header, value, new_line))
            if date_.havdala:
                header, new_line = self._humanize_header_date(headers.havdala, date_.havdala)
                value = humanize_time(date_.havdala.time())
                lines.append((header, value, new_line))

        return lines

    @staticmethod
    def _get_font_properties(number_of_lines: int) -> Tuple[int, int, int]:
        p = {
            # [font_size, y_offset, start_y_position]
            2: (57, 70, 400),
            3: (57, 70, 400),
            4: (55, 70, 400),
            5: (55, 80, 260),
            6: (55, 70, 260),
            7: (55, 70, 260),
            8: (55, 60, 260),
            9: (50, 50, 230),
            10: (50, 50, 230)
        }
        font_size, y_offset, start_position_y = p.get(number_of_lines)
        return start_position_y, y_offset, font_size

    def get_image(self) -> Tuple[BytesIO, Optional[InlineKeyboardMarkup]]:
        x = 80

        dates = self._get_dates()
        lines = self._prepare_lines(dates)
        y, y_offset, font_size = self._get_font_properties(len(lines))
        self._font = ImageFont.truetype(str(self._font_path), size=font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), size=font_size)

        for header, value, new_line in lines:
            if not header:
                y += y_offset * 2
                continue

            self._draw_line(x, y, header, value, new_line)
            if new_line:
                y += self._y_font_offset(header)
            y += y_offset

        kb = get_zmanim_by_date_buttons(
            list(map(
                lambda d: d.date if isinstance(d, AsurBeMelachaDay) else d,
                dates
            ))
        )
        return _convert_img_to_bytes_io(self._image), kb
