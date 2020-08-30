from io import BytesIO
from pathlib import Path
from datetime import datetime as dt, date, time
from typing import Union, Dict, List, Tuple, Optional

from babel.support import LazyProxy
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

from ...middlewares.i18n import gettext as _
from ...zmanim_api.models import *
from ...texts.single import names, headers, helpers
from ...texts.plural import units


IMG_SIZE = 1181
Line = Tuple[Optional[str], Optional[str], Optional[bool]]
EMPTY_LINE = None, None, None


def humanize_date(date_range: List[Union[date, AsurBeMelachaDay]], weekday_on_new_line: bool = False) -> str:
    """
    Use this function for humanize date or date range
    Examples:
      2020-01-01 -> 1 January 2020, Wednesday
      2020-01-01, 2020-01-08 -> 1—7 January 2020, Wednesday-Tuesday
      2020-01-31, 2020-02-1 -> 31 January—1 February 2020, Friday-Saturday
      2019-12-25, 2020-01-03 -> 25 December 2019—3 January 2020, Wednesday-Friday
    """
    weekday_sep = '\n' if weekday_on_new_line else ' '
    months = names.MONTH_NAMES_GENETIVE
    weekdays = names.WEEKDAYS

    d1 = date_range[0]
    d2 = date_range[1] if (len(date_range) > 1) and (date_range[0] != date_range[1]) else None

    if isinstance(d1, AsurBeMelachaDay):
        d1 = d1.date
    if isinstance(d2, AsurBeMelachaDay):
        d2 = d2.date

    if not d2:
        d = d1
        resp = f'{d.day} {months[d.month]} {d.year},{weekday_sep}{weekdays[d.weekday()]}'

    elif d1.year != d2.year:
        resp = f'{d1.day} {months[d1.month]} {d1.year} — ' \
               f'{d2.day} {months[d2.month]} {d2.year}, ' \
               f'{weekdays[d1.weekday()]}-{weekdays[d2.weekday()]}'

    elif d1.month != d2.month:
        resp = f'{d1.day} {months[d1.month]} — {d2.day} {months[d2.month]} {d1.year},{weekday_sep}' \
               f'{weekdays[d1.weekday()]}-{weekdays[d2.weekday()]}'

    else:
        resp = f'{d1.day}-{d2.day} {months[d1.month]} {d1.year},{weekday_sep}' \
               f'{weekdays[d1.weekday()]}-{weekdays[d2.weekday()]}'

    return resp


def humanize_header_date(header_type: str, date_: Union[date, dt]) -> Tuple[str, bool]:
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


def humanize_time(time_: time) -> str:
    """ Use this function for convert time to hh:mm """
    if isinstance(time_, time):
        return time_.isoformat(timespec='minutes')


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
    # smaller font for shmini atzeres
    _title_font_sa = ImageFont.truetype(str(_bold_font_path), 55)
    _font_size = 0
    _warning_font_size = 0
    _background_path = None

    _image: PngImagePlugin.PngImageFile
    _draw: ImageDraw
    # _raw_data = None

    def __init__(self):
        self._font = ImageFont.truetype(str(self._font_path), self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), self._font_size)

        if self._background_path:
            self._image, self._draw = _get_draw(str(self._background_path))

        self._warning_font = ImageFont.truetype(str(self._bold_font_path), self._warning_font_size)

    def _draw_title(self, draw: ImageDraw, title: LazyProxy, is_zmanim: bool = False,
                    is_shmini_atzeres: bool = False) -> None:
        coordinates = (250, 90) if not is_zmanim else (250, 65)
        font = self._title_font if not is_shmini_atzeres else self._title_font_sa
        draw.text(coordinates, title.value, font=font)

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
            value_on_new_line: bool = False
    ):
        header = f'{str(header)}: '
        self._draw.text((x, y), text=header, font=self._bold_font)

        # if not value_on_new_line:
        x += self._x_font_offset(header)
        # else:
        if value_on_new_line:
            y += self._y_font_offset(header.split('\n')[0])

        # TODO: validate that value smaller them picture size
        self._draw.text((x, y), text=str(value), font=self._font)

    def get_image(self) -> BytesIO:
        raise NotImplemented


class DafYomImage(BaseImage):
    def __init__(self, data: DafYomi):
        self._font_size = 90
        self.data = data
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'daf_yomi.png'

        super().__init__()
        self._draw_title(self._draw, names.title_daf_yomi)

    def get_image(self) -> BytesIO:
        y = 470
        x = 100
        y_offset = 100

        # draw masehet
        self._draw_line(x, y, headers.daf_masehet, self.data.masehet)
        y += y_offset

        # draw daf
        self._draw_line(x, y, headers.daf_page, str(self.data.daf))

        return _convert_img_to_bytes_io(self._image)


class RoshChodeshImage(BaseImage):
    def __init__(self, data: RoshChodesh):
        self.data = data
        self._font_size = 46
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'rosh_hodesh.png'

        super().__init__()
        self._draw_title(self._draw, names.title_rosh_chodesh)

    def get_image(self) -> BytesIO:
        y = 370
        x = 100
        y_offset = 80

        # draw month
        self._draw_line(x, y, headers.rh_month, self.data.month_name)
        y += y_offset

        # draw duration
        duration_value = f'{self.data.duration} {_("day", "days", self.data.duration)}'
        self._draw_line(x, y, headers.rh_duration, duration_value)
        y += y_offset

        date_value = humanize_date([self.data.settings.date_])
        self._draw_line(x, y, headers.date, date_value)

        # draw molad string
        molad = self.data.molad[0]
        molad_value = f'{molad.day} {names.MONTH_NAMES_GENETIVE[molad.month]}, {molad.year},\n' \
                      f'{molad.time().hour} {_(*units.tu_hour, molad.time().hour)} ' \
                      f'{molad.time().minute} {_(*units.tu_minute, molad.time().minute)} ' \
                      f'{helpers.and_word} {self.data.molad[1]} {_(*units.tu_part, self.data.molad[1])}'
        self._draw_line(x, y, headers.rh_molad, molad_value)

        return _convert_img_to_bytes_io(self._image)


class ShabbatImage(BaseImage):

    def __init__(self, data: Shabbat):
        self.data = data
        self._font_size = 60
        self._warning_font_size = 48

        super().__init__()

    def draw_picture(self):
        if not self.data.candle_lighting or self.data.late_cl_warning:
            self._background_path: str = Path(__file__).parent / 'res' / 'backgrounds' / 'shabbos_attention.png'
        else:
            self._background_path: str = Path(__file__).parent / 'res' / 'backgrounds' / 'shabbos.png'
        self._image, self._draw = _get_draw(str(self._background_path))

        self._draw_title(self._draw, names.title_shabbath)

        y = 400 if self.data.candle_lighting else 470
        x = 100
        y_offset: int = 80

        # draw parashat hashavua
        self._draw_line(x, y, headers.parsha, self.data.torah_part)
        y += y_offset

        # if polar error, draw error message and return
        if not self.data.candle_lighting:
            x = 100
            y = 840 if helpers.cl_error_warning.value.count('\n') < 2 else 810

            self._draw.text((x, y), helpers.cl_error_warning.value, font=self._warning_font, fill='#ff5959')
            return _convert_img_to_bytes_io(self._image)

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

        # draw warning if need
        if not self.data.late_cl_warning:
            return _convert_img_to_bytes_io(self._image)

        x, y = 100, 840
        self._draw.text((x, y), helpers.cl_late_warning.value, font=self._warning_font, fill='#ff5959')

        return _convert_img_to_bytes_io(self._image)


class ZmanimImage(BaseImage):

    def __init__(self, data: Zmanim):
        self.data = data
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'zmanim.png'
        super().__init__()

        self._draw_title(self._draw, names.title_zmanim, is_zmanim=True)

    def _set_font_properties(self, number_of_lines: int):
        p = {
            # [font_size, y_offset, start_y_offset
            1: [58, 68, 300],
            2: [58, 68, 270],
            3: [58, 68, 220],
            4: [58, 68, 180],
            5: [58, 68, 160],
            6: [58, 68, 140],
            7: [58, 68, 100],
            8: [58, 68, 85],
            9: [58, 68, 85],
            10: [59, 68, 40],
            11: [57, 66, 20],
            12: [55, 64, 20],
            13: [52, 58, 20],
            14: [45, 52, 20],
            15: [43, 50, 10],
            16: [41, 48, 10],
            17: [39, 46, 0],
            18: [37, 44, 0],
            19: [35, 42, 0]
        }
        self._font_size, self._y_offset, self._start_y_offset = p.get(number_of_lines)
        self._font = ImageFont.truetype(str(self._font_path), size=self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), size=self._font_size)

    def _draw_date(self, date_: str):
        x = 250
        y = 130
        date_font = ImageFont.truetype(str(self._font_path), 40)
        self._draw.text((x, y), date_, font=date_font)

    def get_image(self) -> BytesIO:
        zmanim: Dict[str, dt] = self.data.dict(exclude={'settings'}, exclude_none=True)
        self._set_font_properties(len(zmanim))
        self._draw_date(humanize_date([self.data.settings.date_]))

        y: int = 210 + self._start_y_offset
        x: int = 100

        # draw all image lines in cycle
        for header, value in zmanim.items():
            self._draw_line(
                x, y, _(header),
                value.time().isoformat('minutes') if isinstance(value, date) else value.isoformat('minutes')
            )
            y += self._y_offset

        return _convert_img_to_bytes_io(self._image)


class FastImage(BaseImage):

    def __init__(self, data: Fast):
        self.data = data
        self._background_path = Path(__file__).parent / 'res' / 'backgrounds' / 'fast.png'
        self._font_size = 60

        super().__init__()

    def get_image(self) -> BytesIO:
        self._draw_title(self._draw, names.FASTS_TITLES[self.data.settings.fast_name])

        x = 100
        y = 450

        y_offset = 80
        y_offset_sep = 100
        y_offset_sep_small = 70

        # draw date and start time
        fast_date, fast_weekday = humanize_date([self.data.fast_start]).split(', ')
        fast_start_value = f'{fast_date}\n{fast_weekday}, {self.data.fast_start.time().isoformat("minutes")}'
        self._draw_line(x, y, headers.fast_start, fast_start_value)

        # draw hatzot, if need
        if self.data.chatzot:
            y += y_offset_sep_small
            self._draw_line(x, y, headers.fast_chatzot, self.data.chatzot.time().isoformat('minutes'))
            y += y_offset + y_offset_sep_small
        else:
            y += y_offset_sep

        # draw havdala
        self._draw_line(x, y, headers.fast_end, self.data.havdala.time().isoformat('minutes'))

        # timings = [data.tzeit_kochavim, data.sba_time, data.ssk_time, data.nvr_time]
        # for timing in timings:
        #     self._draw_line((pos_x, pos_y), timing.header, timing.value)
        #     pos_y += y_offset

        return _convert_img_to_bytes_io(self._image)


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

        # TODO: add chanukah range days formatting
        self._draw_line(x, y, headers.date, humanize_date([self.data.date, self.data.date]))
        return _convert_img_to_bytes_io(self._image)


class YomTovImage(BaseImage):

    def __init__(self, data: YomTov):
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

    def _prepare_lines(self) -> List[Line]:
        dates = [
            self.data.pre_shabbat,
            self.data.day_1,
            self.data.day_2,
            self.data.post_shabbat,
            self.data.pesach_part_2_day_1,
            self.data.pesach_part_2_day_2,
            self.data.hoshana_rabba
        ]
        dates = [d for d in dates if d is not None]

        lines = []

        for date_ in dates:
            if isinstance(date_, date):
                header = str(headers.hoshana_raba)
                value = f'{date_.day} {names.MONTH_NAMES_GENETIVE[date_.month]} {names.WEEKDAYS[date_.weekday()]}'
                lines.append(EMPTY_LINE)
                lines.append((header, value))
                continue

            if date_ == self.data.pesach_part_2_day_1:
                lines.append(EMPTY_LINE)

            if date_.candle_lighting:
                header, new_line = humanize_header_date(headers.cl, date_.candle_lighting)
                value = humanize_time(date_.candle_lighting.time())
                lines.append((header, value, new_line))
            if date_.havdala:
                header, new_line = humanize_header_date(headers.havdala, date_.havdala)
                value = humanize_time(date_.havdala.time())
                lines.append((header, value, new_line))

        return lines

    @staticmethod
    def _get_font_properties(number_of_lines: int) -> Tuple[int, int, int]:
        p = {
            # [font_size, y_offset, start_y_offset]
            3: (58, 70, 420),
            4: (58, 70, 420),
            5: (58, 70, 420),
            6: (58, 70, 420),
            7: (58, 70, 420),
            8: (58, 70, 420)
        }
        font_size, y_offset, start_position_y = p.get(number_of_lines)
        return start_position_y, y_offset, font_size

    def get_image(self) -> BytesIO:
        # todo case of date with post shabbat
        x = 80

        lines = self._prepare_lines()
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


        # self._image.save('test.png')
        return _convert_img_to_bytes_io(self._image)


# def test():
#     j = {
#   "settings": {
#     "date": "2022-04-15",
#     "cl_offset": 18,
#     "havdala_opinion": "tzeis_8_5_degrees",
#     "coordinates": [
#       55.5,
#       37.7
#     ],
#     "elevation": 0,
#     "yomtov_name": "shavuot"
#   },
#   "pre_shabbat": {
#     "date": "2022-06-04",
#     "candle_lighting": "2022-06-03T20:44:39.375578+03:00"
#   },
#   "day_1": {
#     "date": "2022-06-05",
#     "candle_lighting": "2022-06-04T22:36:39.212694+03:00"
#   },
#   "day_2": {
#     "date": "2022-06-06",
#     "candle_lighting": "2022-06-05T22:38:33.390085+03:00",
#     "havdala": "2022-06-06T22:40:23.180390+03:00"
#   }
# }
#     d = YomTov(**j)
#     YomTovImage(d).get_image()
