from io import BytesIO
from typing import Callable, NoReturn, Tuple
from gettext import translation
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

from ..localizations import *
from ..settings import I18N_DOMAIN


def get_translator(lang: str) -> Callable:
    languages = {'Russian': 'ru', 'English': 'en'}
    loc_path = Path(__file__).parent.parent.parent / 'locales'
    locale = translation(I18N_DOMAIN, loc_path, languages=[languages.get(lang)])
    locale.install()
    return locale.gettext


def _convert_img_to_bytes_io(img: PngImagePlugin.PngImageFile) -> BytesIO:
    bytes_io = BytesIO()
    img.save(bytes_io, 'png')
    bytes_io.seek(0)
    return bytes_io


def _get_draw(background_path: str) -> ImageDraw:
    image = Image.open(background_path)
    draw = ImageDraw.Draw(image)
    return image, draw


class BasePicture:

    _font_path = Path(__file__).parent / 'fonts' / 'gothic.TTF'
    _bold_font_path = Path(__file__).parent / 'fonts' / 'gothic-bold.TTF'
    _title_font = ImageFont.truetype(str(_bold_font_path), 60)
    # smaller font for shmini atzeres
    _title_font_sa = ImageFont.truetype(str(_bold_font_path), 55)
    _font_size = 0
    _warning_font_size = 0
    _background_path = None
    _lang = None
    _translation_func = None
    _raw_data = None

    def __init__(self):
        self._font = ImageFont.truetype(str(self._font_path), self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), self._font_size)
        self._image, self._draw = _get_draw(str(self._background_path))
        self._translator = get_translator(self._lang)
        self._warning_font = ImageFont.truetype(str(self._bold_font_path),
                                                self._warning_font_size)

    def _draw_title(self, draw: ImageDraw, title: str, is_zmanim: bool = False,
                    is_shmini_atzeres: bool = False) -> None:
        coordinates = (250, 90) if not is_zmanim else (250, 65)
        font = self._title_font if not is_shmini_atzeres else self._title_font_sa
        draw.text(coordinates, title, font=font)

    def draw_picture(self) -> NoReturn:
        pass

    def _x_font_offset(self, text: str) -> int:
        return self._bold_font.getsize(text)[0]

    def _y_font_offset(self, text: str) -> int:
        return self._bold_font.getsize(text)[1]

    def _draw_line(self, xy: Tuple[int, int], header: str, value: str,
                   value_on_new_line: bool = False) -> NoReturn:
        header = f'{header}: '
        self._draw.text(xy, text=header, font=self._bold_font)

        if not value_on_new_line:
            xy = xy[0] + self._x_font_offset(header), xy[1]
        else:
            xy = xy[0], xy[1] + self._y_font_offset(header)

        self._draw.text((xy[0], xy[1]), text=value, font=self._font)


class DafYomPicture(BasePicture):
    def __init__(self, lang: str, data: dict) -> NoReturn:
        self._font_size = 90
        self._background_path = 'res/image/backgrounds/daf_yomi.png'
        self._lang = lang

        super().__init__()

        localized_data = daf_yomi.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 470
        pos_x = 100
        y_offset = 100

        data = self._data

        # draw masehet
        self._draw_line((pos_x, pos_y), data.masehet.header, data.masehet.value)
        pos_y += y_offset

        # draw daf
        self._draw_line((pos_x, pos_y), data.daf.header, data.daf.value)

        return _convert_img_to_bytes_io(self._image)


class RoshHodeshPicture(BasePicture):
    def __init__(self, lang: str, data: dict) -> NoReturn:
        self._font_size = 46
        self._background_path = 'res/image/backgrounds/rosh_hodesh.png'
        self._lang = lang

        super().__init__()

        localized_data = rosh_hodesh.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    @staticmethod
    def format_rh_date(days: list, months: list, years: list, dow: list) -> str:
        # todo move to rh module
        day = f'{days[0]}' if len(days) == 1 else f'{days[0]}-{days[1]}'
        month = f'{months[0]}' if len(months) == 1 else f'{months[0]}-{months[1]}'
        year = f'{years[0]}' if len(years) == 1 else f'{years[0]}-{years[1]}'
        dow = f'{dow[0]}' if len(dow) == 1 else f'{dow[0]}-{dow[1]}'

        new_line = '\n' if len(days) > 1 else ' '

        date_str = f'{day} {month} {year},{new_line}{dow}'
        return date_str

    def draw_picture(self) -> BytesIO:
        pos_y = 370
        pos_x = 100
        y_offset = 80

        data = self._data

        # draw month
        self._draw_line((pos_x, pos_y), data.month.header, data.month.value)
        pos_y += y_offset

        # draw number of days (n_days)
        self._draw_line((pos_x, pos_y), data.n_days.header, data.n_days.value)
        pos_y += y_offset

        # prepare date string
        date = data.date  # todo move to rh module
        date_str = self.format_rh_date(date.days, date.months, date.years, date.dow)

        # draw date strings
        self._draw_line((pos_x, pos_y), data.date.header, date_str)
        pos_y += y_offset  # todo test

        # prepare molad string
        molad = data.molad  # todo move to rh module
        molad_str = f'{molad.day} {molad.month}, {molad.dow},\n{molad.n_hours} ' \
                    f'{molad.hours_word} {molad.n_of_minutes} {molad.minutes_word} ' \
                    f'{molad.and_word} {molad.n_parts} {molad.parts_word}'

        # draw molad string
        self._draw_line((pos_x, pos_y), data.molad.header, molad_str)

        return _convert_img_to_bytes_io(self._image)


class ShabbosPicture(BasePicture):

    def __init__(self, lang: str, data: dict) -> NoReturn:
        self._font_size = 60
        self._warning_font_size = 48
        self._lang = lang
        if data['error'] or data['warning']:
            self._background_path: str = 'res/image/backgrounds/shabbos_attention.png'
        else:
            self._background_path: str = 'res/image/backgrounds/shabbos.png'

        super().__init__()

        localized_data = shabbos.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self):
        pos_y = 400 if not self._data.error else 470
        pos_x = 100
        y_offset: int = 80

        font = self._font
        warning_font = self._warning_font
        data = self._data
        draw = self._draw

        # draw parashat hashavua
        self._draw_line((pos_x, pos_y), data.parasha.header, data.parasha.value)
        pos_y += y_offset

        # if polar error, draw error message and return
        if data.error:
            pos_x = 100
            pos_y = 840 if data.error.count('\n') < 2 else 810

            draw.text((pos_x, pos_y), data.error, font=warning_font, fill='#ff5959')
            return _convert_img_to_bytes_io(self._image)

        # draw candle lighting
        self._draw_line((pos_x, pos_y), data.cl.header, data.cl.value)
        pos_y += y_offset

        # draw shekiah offset
        draw.text((pos_x, pos_y), data.shkia_offset, font=font)
        pos_y += y_offset

        # draw tzeis hakochavim
        self._draw_line((pos_x, pos_y), data.tzeit_kochavim.header,
                        data.tzeit_kochavim.value)
        pos_y += y_offset

        # draw warning if need
        if not data.warning:
            return _convert_img_to_bytes_io(self._image)

        pos_x, pos_y = 100, 840
        draw.text((pos_x, pos_y), data.warning, font=warning_font, fill='#ff5959')

        return _convert_img_to_bytes_io(self._image)


class ZmanimPicture(BasePicture):

    def __init__(self, lang: str, data: dict) -> NoReturn:
        self._background_path = 'res/image/backgrounds/zmanim.png'
        self._lang = lang

        localized_data = zmanim.get_translate(data, get_translator(lang))
        self._data = localized_data.zmanim
        self._date = localized_data.date

        self._set_font_properties(len(self._data))
        super().__init__()

        self._draw_title(self._draw, localized_data.title, is_zmanim=True)
        self._draw_date()

    def _set_font_properties(self, number_of_lines: int) -> NoReturn:
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
        self._font = ImageFont.truetype(self._font_path, size=self._font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, size=self._font_size)

    def _draw_date(self) -> NoReturn:
        pos_x = 250
        pos_y = 130
        date_font = ImageFont.truetype(self._font_path, 40)

        self._draw.text((pos_x, pos_y), self._date, font=date_font)

    def draw_picture(self) -> BytesIO:
        pos_y: int = 210 + self._start_y_offset  # todo test
        pos_x: int = 100

        data: dict = self._data

        # draw all zmanim lines in cycle
        for header, value in data.items():
            self._draw_line((pos_x, pos_y), header, value)
            pos_y += self._y_offset

        return _convert_img_to_bytes_io(self._image)


class FastPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/fast.png'
        self._font_size = 60
        self._lang = lang

        super().__init__()

        localized_data = fast.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 290
        pos_x = 100
        y_offset = 80
        y_offset_sep = 100
        y_offset_sep_small = 70

        data = self._data

        # draw date and start time
        self._draw_line((pos_x, pos_y), data.start_time.header, data.start_time.value)
        pos_y += y_offset  # todo test

        # draw hatzot, if need
        if data.hatzot:
            pos_y += y_offset_sep_small
            self._draw_line((pos_x, pos_y), data.hatzot.header, data.hatzot.value)
            pos_y += y_offset + y_offset_sep_small
        else:
            pos_y += y_offset_sep

        timings = [data.tzeit_kochavim, data.sba_time, data.ssk_time, data.nvr_time]
        for timing in timings:
            self._draw_line((pos_x, pos_y), timing.header, timing.value)
            pos_y += y_offset

        return _convert_img_to_bytes_io(self._image)


class RoshHashanaPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/rosh_hashana.png'
        self._font_size = 47
        self._lang = lang

        super().__init__()

        localized_data = yom_tov.get_translate(data, self._translator, 'rosh_hashana')
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 400
        pos_x = 100
        y_offset = 95
        y_offset_small = 65

        data = self._data

        # draw the date
        self._draw_line((pos_x, pos_y), data.date.header, data.date.value)
        pos_y += y_offset + self._y_font_offset(data.date.value)

        # draw candle lightings and havdala
        days = [data.cl_1, data.cl_2, data.cl_3, data.havdala]  # todo replicate

        for day in days:
            # if there is no third day (shabbos)
            if not day:
                continue

            self._draw_line((pos_x, pos_y), day.header, day.value)
            pos_y += y_offset_small

        return _convert_img_to_bytes_io(self._image)


class YomKippurPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/yom_kippur.png'
        self._font_size = 55
        self._lang = lang

        super().__init__()

        localized_data = yom_kippur.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 300
        pos_x = 100
        y_offset = 170
        y_offset_small = 90

        data = self._data

        # draw date
        self._draw_line((pos_x, pos_y), data.date.header, data.date.value)
        pos_y += y_offset

        # draw candle lightning
        self._draw_line((pos_x, pos_y), data.cl.header, data.cl.value,  True)
        pos_y += y_offset_small

        # draw havdala
        self._draw_line((pos_x, pos_y), data.havdala.header, data.havdala.value, True)
        pos_y += y_offset_small

        return _convert_img_to_bytes_io(self._image)


class SucosPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/succos.png'
        self._font_size = 47
        self._lang = lang

        super().__init__()

        localized_data = succos.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 300
        pos_x = 100
        y_offset = 100
        y_offset_small = 65

        data = self._data

        # draw the date
        self._draw_line((pos_x, pos_y), data.date.header, data.date.value)
        pos_y += y_offset

        # draw cl 1
        self._draw_line((pos_x, pos_y), data.cl_1.header, data.cl_1.value)
        pos_y += y_offset_small

        # draw cl 2 if it exist
        self._draw_line((pos_x, pos_y), data.cl_2.header, data.cl_2.value)
        pos_y += y_offset_small

        # draw cl 3 if it exist
        if data.cl_3:
            self._draw_line((pos_x, pos_y), data.cl_3.header, data.cl_3.value)
            pos_y += y_offset_small

        # draw havdala
        self._draw_line((pos_x, pos_y), data.havdala.header, data.havdala.value)
        pos_y += y_offset

        # draw hoshana raba
        self._draw_line((pos_x, pos_y), data.hoshana_raba.header, data.hoshana_raba.value)

        return _convert_img_to_bytes_io(self._image)


class ShminiAtzeretPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/shmini_atzeret.png'
        self._font_size = 45
        self._lang = lang

        super().__init__()

        localized_data = shmini_atzeres.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title, is_shmini_atzeres=True)

    def draw_picture(self) -> BytesIO:
        pos_y = 400
        pos_x = 100
        y_offset = 100
        y_offset_small = 65

        data = self._data

        # draw the date
        self._draw_line((pos_x, pos_y), data.date.header, data.date.value)
        pos_y += y_offset + self._y_font_offset(data.date.value)

        # draw cl 1
        self._draw_line((pos_x, pos_y), data.cl_1.header, data.cl_1.value)
        pos_y += y_offset_small

        # draw cl 2 if it exist
        if data.cl_2:
            self._draw_line((pos_x, pos_y), data.cl_2.header, data.cl_2.value)
            pos_y += y_offset_small

        # draw cl 3 if it exist
        if data.cl_3:
            self._draw_line((pos_x, pos_y), data.cl_3.header, data.cl_3.value)
            pos_y += y_offset_small

        # draw havdala
        self._draw_line((pos_x, pos_y), data.havdala.header, data.havdala.value)
        pos_y += y_offset

        return _convert_img_to_bytes_io(self._image)


class ChanukaPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/chanuka.png'
        self._font_size = 60
        self._lang = lang

        super().__init__()

        localized_data = channukah.get_translate(data, self._translator)
        self._data = localized_data.date
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 450
        pos_x = 100

        data = self._data
        self._draw_line((pos_x, pos_y), data.header, data.value)
        return _convert_img_to_bytes_io(self._image)


class TuBiShvatPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/tubishvat.png'
        self._font_size = 70
        self._lang = lang

        super().__init__()

        localized_data = tu_bishvat.get_translate(data, self._translator)
        self._data = localized_data.date
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 450
        pos_x = 100

        data = self._data
        self._draw_line((pos_x, pos_y), data.header, data.value)
        return _convert_img_to_bytes_io(self._image)


class PurimPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/purim.png'
        self._font_size = 70
        self._lang = lang

        super().__init__()

        localized_data = purim.get_translate(data, self._translator)
        self._data = localized_data.date
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 450
        pos_x = 100

        data = self._data
        self._draw_line((pos_x, pos_y), data.header, data.value)
        return _convert_img_to_bytes_io(self._image)


class PesahPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/pesah.png'
        self._font_size = 43 if data['part_1']['day_3'] else 50
        self._lang = lang

        super().__init__()

        localized_data = pesach.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        # shortcuts for code glance
        date = self._data.date
        part_1 = self._data.part_1
        part_2 = self._data.part_2
        draw = self._draw_line

        pos_y = 250 if part_1.cl_3 else 270
        pos_x = 100
        y_offset = 70
        y_offset_small = 65

        # draw the date
        draw((pos_x, pos_y), date.header, date.value)
        pos_y += y_offset + self._y_font_offset(date.value)

        # draw part 1: candle lighting(-s) and havdala
        lines = [part_1.cl_1, part_1.cl_2, part_1.cl_3, part_1.havdala]
        for line in lines:
            if not line:
                continue
            draw((pos_x, pos_y), line.header, line.value)
            pos_y += y_offset_small

        pos_y += y_offset

        # draw part 2: candle lighting(-s) and havdala
        lines = [part_2.cl_1, part_2.cl_2, part_2.cl_3, part_2.havdala]
        for line in lines:
            if not line:
                continue
            draw((pos_x, pos_y), line.header, line.value)
            pos_y += y_offset_small

        return _convert_img_to_bytes_io(self._image)


class LagBaomerPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/lagbaomer.png'
        self._font_size = 70
        self._lang = lang

        super().__init__()

        localized_data = lag_baomer.get_translate(data, self._translator)
        self._data = localized_data.date
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self):
        pos_y = 450
        pos_x = 100

        data = self._data
        self._draw_line((pos_x, pos_y), data.header, data.value)

        return _convert_img_to_bytes_io(self._image)


class ShavuotPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/shavuot.png'
        self._font_size = 45
        self._lang = lang

        super().__init__()

        localized_data = yom_tov.get_translate(data, self._translator, 'shavuos')
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 400
        pos_x = 100
        y_offset = 95
        y_offset_small = 65

        data = self._data

        # draw the date
        self._draw_line((pos_x, pos_y), data.date.header, data.date.value)
        pos_y += y_offset + self._y_font_offset(data.date.value)

        # draw candle lightings and havdala
        days = [data.cl_1, data.cl_2, data.cl_3, data.havdala]

        for day in days:
            # if there is no third day (shabbos)
            if not day:
                continue

            self._draw_line((pos_x, pos_y), day.header, day.value)
            pos_y += y_offset_small

        return _convert_img_to_bytes_io(self._image)


class IsraelHolidaysPicture(BasePicture):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/israel_holidays.png'
        self._font_size = 50
        self._lang = lang

        super().__init__()

        localized_data = israel_holidays.get_translate(data, self._translator)
        self._data = localized_data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self):
        pos_y = 320
        pos_x = 100
        y_offset = 80
        y_offset_small = 60

        data = self._data

        holidays = [data.yom_hashoa, data.yom_hazikaron, data.yom_haatzmaaut,
                    data.yom_yerushalaim]

        for holiday in holidays:
            self._draw_line((pos_x, pos_y), holiday.title, '')
            pos_y += y_offset_small
            self._draw_line((pos_x, pos_y), holiday.date.header, holiday.date.value)
            pos_y += y_offset

        return _convert_img_to_bytes_io(self._image)


def get_picture(picture_type: str):
    picture_types = {
        'zmanim': ZmanimPicture,
        'shabbos': ShabbosPicture,
        'rosh_chodesh': RoshHodeshPicture,
        'daf_yomi': DafYomPicture,
        'rosh_hashana': RoshHashanaPicture,
        'yom_kippur': YomKippurPicture,
        'succos': SucosPicture,
        'shmini_atseres': ShminiAtzeretPicture,
        'chanukah': ChanukaPicture,
        'purim': PurimPicture,
        'pesach': PesahPicture,
        'shavuos': ShavuotPicture,
        'tu_bishvat': TuBiShvatPicture,
        'lag_baomer': LagBaomerPicture,
        'israel_holidays': IsraelHolidaysPicture,
        'fast': FastPicture,
    }
    picture_class = picture_types.get(picture_type)
    return picture_class
