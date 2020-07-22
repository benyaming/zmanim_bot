from io import BytesIO
from pathlib import Path
from datetime import datetime as dt, date, time
from typing import Union, Dict, List, Any

from babel.support import LazyProxy
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

from ...middlewares.i18n import gettext as _
from ...zmanim_api.models import *
from ...texts.single import names, headers, helpers
from ...texts.plural import units


def humanize_date(date_range: List[Union[date, AsurBeMelachaDay]], weekday_on_new_line: bool = False) -> str:
    """
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


def get_header_with_date(header_type: str, date_: Union[date, dt], cl: bool = False) -> str:
    """

    :param header_type: `headers.cl` or `headers.havdala`
    :param date_:
    :param cl:
    :return:
    """
    if header_type == headers.cl and date_.weekday() == 4:
        shabbat = f' ({names.shabbat})'
    else:
        shabbat = ''

    resp = f'{header_type} {date_.day} {names.MONTH_NAMES_GENETIVE[date_.month]}{shabbat}'
    return resp


def _format_value(value: Union[str, int, float, dt, date, time, LazyProxy]) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, LazyProxy):
        return value.value
    elif isinstance(value, float):
        return str(round(value, 2))


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

    _font_path = Path(__file__).parent / 'src' / 'fonts' / 'gothic.TTF'
    _bold_font_path = Path(__file__).parent / 'src' / 'fonts' / 'gothic-bold.TTF'
    _title_font = ImageFont.truetype(str(_bold_font_path), 60)
    # smaller font for shmini atzeres
    _title_font_sa = ImageFont.truetype(str(_bold_font_path), 55)
    _font_size = 0
    _warning_font_size = 0
    _background_path = None
    _raw_data = None

    def __init__(self):
        self._font = ImageFont.truetype(str(self._font_path), self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), self._font_size)

        if self._background_path:
            self._image, self._draw = _get_draw(str(self._background_path))

        self._warning_font = ImageFont.truetype(str(self._bold_font_path),
                                                self._warning_font_size)

    def _draw_title(self, draw: ImageDraw, title: LazyProxy, is_zmanim: bool = False,
                    is_shmini_atzeres: bool = False) -> None:
        coordinates = (250, 90) if not is_zmanim else (250, 65)
        font = self._title_font if not is_shmini_atzeres else self._title_font_sa
        draw.text(coordinates, title.value, font=font)

    def _x_font_offset(self, text: str) -> int:
        """Returns size in px of given text in axys x"""
        return self._bold_font.getsize(text)[0]

    def _y_font_offset(self, text: str) -> int:
        """Returns size in px of given text in axys y"""
        return self._bold_font.getsize(text)[1]

    def _draw_line(
            self,
            x: int,
            y: int,
            header: Union[LazyProxy, str],
            value: Union[int, str, float, dt, date, time, LazyProxy],
            value_on_new_line: bool = False
    ):
        if isinstance(value, time):
            value = value.isoformat(timespec='minutes')
        elif isinstance(value, date):
            value = humanize_date([value], weekday_on_new_line=False)
        # elif isinstance(value, dt):
        #     value = f''
        # if isinstance(value, LazyProxy):
        #     value = value.value
        # if isinstance(value, int):
        #     value = str(value)

        header = f'{str(header)}: '
        self._draw.text((x, y), text=header, font=self._bold_font)

        if not value_on_new_line:
            x += self._x_font_offset(header)
        else:
            y += self._y_font_offset(header)

        # TODO: validate that value smaller them picture size
        self._draw.text((x, y), text=str(value), font=self._font)

    def get_image(self) -> BytesIO:
        raise NotImplemented


class DafYomImage(BaseImage):
    def __init__(self):
        self._font_size = 90
        self._background_path = Path(__file__).parent / 'src' / 'backgrounds' / 'daf_yomi.png'

        super().__init__()
        self._draw_title(self._draw, names.title_daf_yomi)

    def get_image(self, data: DafYomi) -> BytesIO:
        y = 470
        x = 100
        y_offset = 100

        # draw masehet
        self._draw_line(x, y, headers.daf_masehet, data.masehet)
        y += y_offset

        # draw daf
        self._draw_line(x, y, headers.daf_page, data.daf)

        return _convert_img_to_bytes_io(self._image)


class RoshChodeshImage(BaseImage):
    def __init__(self):
        self._font_size = 46
        self._background_path = Path(__file__).parent / 'src' / 'backgrounds' / 'rosh_hodesh.png'

        super().__init__()
        self._draw_title(self._draw, names.title_rosh_chodesh)

    def get_image(self, data: RoshChodesh) -> BytesIO:
        y = 370
        x = 100
        y_offset = 80

        # draw month
        self._draw_line(x, y, headers.rh_month, data.month_name)
        y += y_offset

        # draw duration
        duration_value = f'{data.duration} {_("day", "days", data.duration)}'
        self._draw_line(x, y, headers.rh_duration, duration_value)
        y += y_offset

        date_value = humanize_date(data.settings.date_)
        self._draw_line(x, y, headers.date, date_value)
        y += y_offset  # todo test

        # draw molad string
        molad = data.molad[0]
        molad_value = f'{molad.day} {names.MONTH_NAMES_GENETIVE[molad.month]}, {molad.year},\n' \
                      f'{molad.time().hour} {_(*units.tu_hour, molad.time().hour)} ' \
                      f'{molad.time().minute} {_(*units.tu_minute, molad.time().minute)} ' \
                      f'{helpers.and_word} {data.molad[1]} {_(*units.tu_part, data.molad[1])}'
        self._draw_line(x, y, headers.rh_molad, molad_value)

        return _convert_img_to_bytes_io(self._image)


class ShabbatImage(BaseImage):

    def __init__(self):
        self._font_size = 60
        self._warning_font_size = 48

        super().__init__()

    def draw_picture(self, data: Shabbat):
        if not data.candle_lighting or data.late_cl_warning:
            self._background_path: str = Path(__file__).parent / 'src' / 'backgrounds' / 'shabbos_attention.png'
        else:
            self._background_path: str = Path(__file__).parent / 'src' / 'backgrounds' / 'shabbos.png'
        self._image, self._draw = _get_draw(str(self._background_path))

        self._draw_title(self._draw, names.title_shabbath)

        y = 400 if data.candle_lighting else 470
        x = 100
        y_offset: int = 80

        # draw parashat hashavua
        self._draw_line(x, y, headers.parsha, data.torah_part)
        y += y_offset

        # if polar error, draw error message and return
        if not data.candle_lighting:
            x = 100
            y = 840 if helpers.cl_error_warning.value.count('\n') < 2 else 810

            self._draw.text((x, y), helpers.cl_error_warning.value, font=self._warning_font, fill='#ff5959')
            return _convert_img_to_bytes_io(self._image)

        # draw candle lighting
        self._draw_line(x, y, headers.cl, data.candle_lighting.time())
        y += y_offset

        # draw shekiah offset
        cl_offset = data.settings.cl_offset
        offset_value = f'({cl_offset} {_(*units.tu_minute, cl_offset)} {helpers.cl_offset})'
        self._draw.text((x, y), offset_value, font=self._font)
        y += y_offset

        # draw havdala
        self._draw_line(x, y, headers.havdala, data.havdala.time())
        y += y_offset

        # draw warning if need
        if not data.late_cl_warning:
            return _convert_img_to_bytes_io(self._image)

        x, y = 100, 840
        self._draw.text((x, y), helpers.cl_late_warning.value, font=self._warning_font, fill='#ff5959')

        return _convert_img_to_bytes_io(self._image)


class ZmanimImage(BaseImage):

    def __init__(self):
        self._background_path = Path(__file__).parent / 'src' / 'backgrounds' / 'zmanim.png'
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

    def get_image(self, data: Zmanim) -> BytesIO:
        zmanim: Dict[str, dt] = data.dict(exclude={'settings'}, exclude_none=True)
        self._set_font_properties(len(zmanim))
        self._draw_date(humanize_date(data.settings.date_))

        y: int = 210 + self._start_y_offset  # todo test
        x: int = 100

        # draw all image lines in cycle
        for header, value in zmanim.items():
            self._draw_line(x, y, _(header), value.time())
            y += self._y_offset

        return _convert_img_to_bytes_io(self._image)


class FastImage(BaseImage):

    def __init__(self):
        self._background_path = Path(__file__).parent / 'src' / 'backgrounds' / 'fast.png'
        self._font_size = 60

        super().__init__()

    def get_image(self, data: Fast) -> BytesIO:
        self._draw_title(self._draw, names.FASTS_TITLES[data.settings.fast_name])

        x = 100
        y = 450

        y_offset = 80
        y_offset_sep = 100
        y_offset_sep_small = 70

        # draw date and start time
        fast_date, fast_weekday = humanize_date(data.fast_start).split(', ')
        fast_start_value = f'{fast_date}\n{fast_weekday}, {data.fast_start.time().isoformat("minutes")}'
        self._draw_line(x, y, headers.fast_start, fast_start_value)
        y += y_offset  # todo test

        # draw hatzot, if need
        if data.chatzot:
            y += y_offset_sep_small
            self._draw_line(x, y, headers.fast_chatzot, data.chatzot.time().isoformat('minutes'))
            y += y_offset + y_offset_sep_small
        else:
            y += y_offset_sep

        # draw havdala
        self._draw_line(x, y, headers.fast_end, data.havdala.time())

        # timings = [data.tzeit_kochavim, data.sba_time, data.ssk_time, data.nvr_time]
        # for timing in timings:
        #     self._draw_line((pos_x, pos_y), timing.header, timing.value)
        #     pos_y += y_offset

        return _convert_img_to_bytes_io(self._image)


class HolidayImage(BaseImage):

    def __init__(self, data: Holiday):
        background_and_font_params = {
            'chanukah': ('chanuka.png', 60),
            'tu_bi_shvat': ('tubishvat.png', 70),
            'purim': ('purim.png', 70),
            'lag_baomer': ('lagbaomer.png', 70),
            'israel_holidays': ('israel_holidays.png', 50),
        }
        background, font_size = background_and_font_params[data.settings.holiday_name]

        self._background_path = Path(__file__).parent / 'src' / 'backgrounds' / background
        self._font_size = font_size

        super().__init__()

        self._data = data
        self._draw_title(self._draw, names.HOLIDAYS_TITLES[data.settings.holiday_name])

    def get_image(self) -> BytesIO:
        x = 100
        y = 450

        # TODO: add chanukah range days formatting
        self._draw_line(x, y, headers.date, self._data.date)
        return _convert_img_to_bytes_io(self._image)


class YomTovImage(BaseImage):

    def __init__(self, data: YomTov):
        background_and_font_params = {
            'rosh_hashana': ('rosh_hashana.png', 47),
            'yom_kippur': ('yom_kippur.png', 55),
            'succot': ('succos.png', 47),
            'shmini_atzeres': ('shmini_atzeret.png', 45),
            'pesach': ('pesah.png', 43 if data.post_shabbat or data.post_shabbat else 50),
            'shavuot': ('shavuot.png', 45),
        }
        background, font_size = background_and_font_params[data.settings.yomtov_name]

        self._background_path = Path(__file__).parent / 'src' / 'backgrounds' / background
        self._font_size = font_size

        super().__init__()

        self.data = data
        self._draw_title(self._draw, names.YOMTOVS_TITLES[data.settings.yomtov_name])

    def get_image(self) -> BytesIO:
        x = 80
        y = 250
        y_offset = 70
        y_offset_small = 65

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

        # draw the date
        start_date = dates[0]
        end_date = dates[-1]

        self._draw_line(x, y, headers.date, humanize_date([start_date, end_date], weekday_on_new_line=True))
        y += y_offset * 2

        for i, date_ in enumerate(dates):
            if isinstance(date_, date):
                self._draw_line(x, y, headers.hoshana_raba, date_)
                continue

            if date_ == self.data.pesach_part_2_day_1:
                y += y_offset_small

            if date_.candle_lighting:
                header = get_header_with_date(headers.cl, date_.candle_lighting)
                self._draw_line(x, y, header, date_.candle_lighting.time())
                y += y_offset_small
            if date_.havdala:
                header = get_header_with_date(headers.havdala, date_.havdala)
                self._draw_line(x, y, header, date_.havdala.time())
                y += y_offset * 1.5


        #
        # for i, date_ in enumerate(dates):
        #     if isinstance(date_, date):  # eve
        #     #     header = get_header_with_date(headers.cl, date_)
        #     #     self._draw_line(x, y, header, dates[i + 1])
        #     #     y += y_offset_small
        #         continue
        #
        #     if date_.candle_lighting:
        #         header = get_header_with_date(headers.cl, date_.candle_lighting.date(), cl=True)
        #         self._draw_line(x, y, header, date_.candle_lighting.time().isoformat('minutes'))
        #         y += y_offset_small
        #
        #     if date_.havdala:
        #         header = get_header_with_date(headers.havdala, date_.havdala.date())
        #         self._draw_line(x, y, header, date_.havdala.time().isoformat('minutes'))
        #         y += y_offset_small


        ###
        #
        ###

        return _convert_img_to_bytes_io(self._image)

