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


def format_header(header: str) -> str:
    return f'{header}: '


class PictureFactory:

    _font_path = Path(__file__).parent / 'fonts' / 'gothic.TTF'
    _bold_font_path = Path(__file__).parent / 'fonts' / 'gothic-bold.TTF'
    _title_font = ImageFont.truetype(str(_bold_font_path), 60)
    # smaller font for shmini atzeres
    _title_font_sa = ImageFont.truetype(str(_bold_font_path), 55)
    # _bold_font = None
    _font_size = 0
    _warning_font_size = 0
    _background_path = None
    _lang = None
    _translation_func = None
    _raw_data = None

    def __init__(self) -> NoReturn:
        self._font = ImageFont.truetype(str(self._font_path), self._font_size)
        self._bold_font = ImageFont.truetype(str(self._bold_font_path), self._font_size)
        self._draw = self._get_draw(str(self._background_path))
        self._translator = get_translator(self._lang)
        self._warning_font = ImageFont.truetype(str(self._bold_font_path),
                                                self._warning_font_size)

    @staticmethod
    def _convert_img_to_bytes_io(img: PngImagePlugin.PngImageFile) -> BytesIO:
        bytes_io = BytesIO()
        img.save(bytes_io, 'png')
        bytes_io.seek(0)
        return bytes_io

    def _get_image(self, background_path) -> Image:
        self._image = Image.open(background_path)
        return self._image

    def _get_draw(self, background_path: str) -> ImageDraw:
        background = self._get_image(background_path)
        draw = ImageDraw.Draw(background)
        return draw

    def _draw_title(self, draw: ImageDraw, title: str, is_zmanim: bool = False,
                    is_shmini_atzeres: bool = False) -> None:
        coordinates = (250, 90) if not is_zmanim else (250, 65)
        font = self._title_font if not is_shmini_atzeres else self._title_font_sa
        draw.text(coordinates, title, font=font)

    @staticmethod
    def get_picture(picture_type, lang, text) -> Callable:
        return picture_type.value(lang, text).draw_picture()

    def draw_picture(self) -> NoReturn:
        pass

    def _font_offset(self, text: str) -> int:
        return self._bold_font.getsize(text)[0]

    def _y_font_offset(self, text: str) -> int:
        return self._bold_font.getsize(text)[1]

    def _draw_line(self, xy: Tuple[int, int], header: str, value: str) -> NoReturn:
        header = format_header(header)
        self._draw.text(xy, text=header, font=self._bold_font)
        self._draw.text((xy[0] + self._font_offset(header), xy[1]), text=value,
                        font=self._font)


class DafYomPicture(PictureFactory):
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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        print(data)

        # draw masehet
        masehet_header = format_header(data.masehet.header)
        masehet_offset = font_offset(masehet_header)

        draw.text((pos_x, pos_y), masehet_header, font=bold_font)
        draw.text((pos_x + masehet_offset, pos_y), data.masehet.value, font=font)
        pos_y += y_offset

        # draw daf
        daf_header = format_header(data.daf.header)
        daf_offset = font_offset(daf_header)

        draw.text((pos_x, pos_y), daf_header, font=bold_font)
        draw.text((pos_x + daf_offset, pos_y), data.daf.value, font=font)

        return self._convert_img_to_bytes_io(self._image)


class RoshHodeshPicture(PictureFactory):
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

        # shortcuts for code glance
        font_offset = self._font_offset
        y_font_offset = self._y_font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        # draw month
        month_header = format_header(data.month.header)
        month_value = data.month.value
        offset = font_offset(month_header)
        draw.text((pos_x, pos_y), month_header, font=bold_font)
        draw.text((pos_x + offset, pos_y), month_value, font=font)
        pos_y += y_offset

        # draw number of days (n_days)
        n_days_header = format_header(data.n_days.header)
        n_days_value = data.n_days.value
        offset = font_offset(n_days_header)
        draw.text((pos_x, pos_y), n_days_header, font=bold_font)
        draw.text((pos_x + offset, pos_y), str(n_days_value), font=font)
        pos_y += y_offset

        # prepare date string
        date = data.date
        date_str = self.format_rh_date(date.days, date.months, date.years, date.dow)
        print(date_str)

        # draw date strings
        date_header = format_header(date.header)
        x_offset = font_offset(date_header)
        optional_y_offset = y_font_offset(date_str) if '\n' in date_str else 0

        draw.text((pos_x, pos_y), date_header, font=bold_font)
        draw.text((pos_x + x_offset, pos_y), date_str, font=font)
        pos_y += y_offset + optional_y_offset

        # prepare molad string
        molad = data.molad
        molad_str1 = f'{molad.day} {molad.month}, {molad.dow},\n{molad.n_hours} ' \
                     f'{molad.hours_word} {molad.n_of_minutes} {molad.minutes_word} ' \
                     f'{molad.and_word} {molad.n_parts} {molad.parts_word}'

        # draw molad string
        molad_header = format_header(molad.header)
        offset = font_offset(molad_header)

        draw.text((pos_x, pos_y), molad_header, font=bold_font)
        draw.text((pos_x + offset, pos_y), molad_str1, font=font)

        return self._convert_img_to_bytes_io(self._image)


class ShabbosPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        warning_font = self._warning_font
        data = self._data
        draw = self._draw

        # draw parashat hashavua
        header = format_header(data.parasha.header)
        value = data.parasha.value
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), value, font=font)
        pos_y += y_offset

        # if polar error, draw error message and return
        if data.error:
            pos_x = 100
            pos_y = 840 if data.error.count('\n') < 2 else 810

            draw.text((pos_x, pos_y), data.error, font=warning_font, fill='#ff5959')
            return self._convert_img_to_bytes_io(self._image)

        # draw candle lighting
        header = format_header(data.candle_lighting.header)
        value = data.candle_lighting.value
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), value, font=font)
        pos_y += y_offset

        # draw shekiah offset
        draw.text((pos_x, pos_y), data.shkia_offset, font=font)
        pos_y += y_offset

        # draw tzeis hakochavim
        header = format_header(data.tzeit_kochavim.header)
        value = data.tzeit_kochavim.value
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), value, font=font)
        pos_y += y_offset

        # draw warning if need
        if not data.warning:
            return self._convert_img_to_bytes_io(self._image)

        pos_x, pos_y = 100, 840
        draw.text((pos_x, pos_y), data.warning, font=warning_font, fill='#ff5959')

        return self._convert_img_to_bytes_io(self._image)


class ZmanimPicture(PictureFactory):

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
        pos_y: int = 210
        pos_x: int = 100

        # shortcuts for code glance
        font_offset: Callable = self._font_offset
        font: ImageFont = self._font
        bold_font: ImageFont = self._bold_font
        data: dict = self._data
        draw: ImageDraw = self._draw

        y_offset: int = self._y_offset
        pos_y += self._start_y_offset

        # draw all zmanim lines in cycle
        for header, value in data.items():
            header = format_header(header)
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), value, font=font)
            pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class FastPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        # draw date and start time
        header = format_header(data.start_time.header)
        header_offset = font_offset(header)
        value_y_offset = self._y_font_offset(data.start_time.value)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.start_time.value, font=font)
        pos_y += y_offset + value_y_offset

        # draw hatzot, if need
        if data.hatzot:
            pos_y += y_offset_sep_small

            header = format_header(data.hatzot.header)
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), data.hatzot.value, font=font)
            pos_y += y_offset + y_offset_sep_small
        else:
            pos_y += y_offset_sep

        # draw 4 end times in cycle
        headers = [
            format_header(data.tzeit_kochavim.header),
            format_header(data.sba_time.header),
            format_header(data.ssk_time.header),
            format_header(data.nvr_time.header)
        ]
        values = [
            data.tzeit_kochavim.value,
            data.sba_time.value,
            data.ssk_time.value,
            data.nvr_time.value
        ]

        for header, value in zip(headers, values):
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), value, font=font)

            pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class RoshHashanaPicture(PictureFactory):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/rosh_hashana.png'
        self._font_size = 47
        self._lang = lang

        super().__init__()

        localized_data = rosh_hashana.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 400
        pos_x = 100
        y_offset = 95
        y_offset_small = 65

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        # draw the date
        header = format_header(data.date.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.date.value, font=font)

        pos_y += y_offset + self._y_font_offset(data.date.value)

        # draw candle lightings and havdala
        days = [data.candle_lighting_1, data.candle_lighting_2, data.candle_lighting_3,
                data.havdalah]

        for day in days:
            # if there is no third day (shabbos)
            if not day:
                continue

            header = format_header(day.header)
            header_offset = font_offset(header.split('\n')[0])

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), day.value, font=font)
            pos_y += y_offset_small

        return self._convert_img_to_bytes_io(self._image)


class YomKippurPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        # draw date
        header = format_header(data.date.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.date.value, font=font)
        pos_y += y_offset

        # draw candle lightning
        header = format_header(data.candle_lighting.header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        pos_y += self._y_font_offset(header)
        draw.text((pos_x, pos_y), data.candle_lighting.value, font=font)
        pos_y += y_offset_small

        # draw havdala
        header = format_header(data.havdala.header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        pos_y += self._y_font_offset(header)
        draw.text((pos_x, pos_y), data.havdala.value, font=font)
        pos_y += y_offset_small

        return self._convert_img_to_bytes_io(self._image)


class SucosPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        # draw the date
        header = format_header(data.date.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.date.value, font=font)
        pos_y += y_offset + self._y_font_offset(data.date.value)

        # draw cl 1
        header = format_header(data.candle_lighting_1.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.candle_lighting_1.value, font=font)
        pos_y += y_offset_small

        # draw cl 2 if it exist
        if data.candle_lighting_2:
            header = format_header(data.candle_lighting_2.header)
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), data.candle_lighting_2.value,
                      font=font)
            pos_y += y_offset_small

        # draw cl 3 if it exist
        if data.candle_lighting_3:
            header = format_header(data.candle_lighting_3.header)
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), data.candle_lighting_3.value,
                      font=font)
            pos_y += y_offset_small

        # draw havdala
        header = format_header(data.havdala.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.havdala.value, font=font)
        pos_y += y_offset

        # draw hoshana raba
        header = format_header(data.hoshana_raba.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.hoshana_raba.value, font=font)

        return self._convert_img_to_bytes_io(self._image)


class ShminiAtzeretPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        # draw the date
        header = format_header(data.date.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.date.value, font=font)
        pos_y += y_offset + self._y_font_offset(data.date.value)

        # draw cl 1
        header = format_header(data.cl_1.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.cl_1.value,
                  font=font)
        pos_y += y_offset_small

        # draw cl 2 if it exist
        if data.cl_2:
            header = format_header(data.cl_2.header)
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), data.cl_2.value,
                      font=font)
            pos_y += y_offset_small

        # draw cl 3 if it exist
        if data.cl_3:
            header = format_header(data.cl_3.header)
            header_offset = font_offset(header)

            draw.text((pos_x, pos_y), header, font=bold_font)
            draw.text((pos_x + header_offset, pos_y), data.cl_3.value,
                      font=font)
            pos_y += y_offset_small

        # draw havdala
        header = format_header(data.havdala.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), data.havdala.value, font=font)
        pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class ChanukaPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        header = format_header(data.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), text=header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), text=data.value, font=font)

        return self._convert_img_to_bytes_io(self._image)


class TuBiShvatPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        header = format_header(data.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), text=header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), text=data.value, font=font)

        return self._convert_img_to_bytes_io(self._image)


class PurimPicture(PictureFactory):

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

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        data = self._data
        draw = self._draw

        header = format_header(data.header)
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), text=header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), text=data.value, font=font)

        return self._convert_img_to_bytes_io(self._image)


class PesahPicture(PictureFactory):

    def __init__(self, lang: str, data: dict):
        self._background_path = 'res/image/backgrounds/pesah.png'
        self._font_size = 50
        self._lang = lang
        # font_size = 43 if lang == 'English' or '(' not in text else 50

        super().__init__()

        localized_data = pesach.get_translate(data, self._translator)
        self._data = localized_data.data
        self._draw_title(self._draw, localized_data.title)

    def draw_picture(self) -> BytesIO:
        pos_y = 270
        pos_x = 100
        y_offset = 100
        y_offset_small = 65

        # shortcuts for code glance
        date = self._data.date
        part_1 = self._data.part_1
        part_2 = self._data.part_2
        draw = self._draw_line

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

        return self._convert_img_to_bytes_io(self._image)



class LagBaomerPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/lagbaomer.png'
        font_size = 70
        title = 'LAG BAOMER TEST'  # TODO title

        self._text = text
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 450
        pos_x = 100
        y_offset_small = 75

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        text = self._text
        draw = self._draw

        # due to non-standart structure of this picture let's draw it manually
        date_header = text.split('|')[0]
        header_offset = font_offset(date_header)
        date, days = text.split('|')[1].split('^')

        # draw date header
        draw.text((pos_x, pos_y), date_header, font=bold_font)
        # draw date
        draw.text((pos_x + header_offset, pos_y), date, font=font)
        pos_y += y_offset_small
        # draw days
        draw.text((pos_x + header_offset, pos_y), days, font=font)

        return self._convert_img_to_bytes_io(self._image)


class ShavuotPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/shavuot.png'
        font_size = 45
        title = 'SHAVUOS TEST'  # TODO title

        self._lines = text.split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 300
        pos_x = 100
        y_offset = 70
        y_offset_small = 65

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        for line in lines:
            # headers separetes from values by '|' symbol
            header, value = line.split('|')
            header_offset = font_offset(header)

            # draw header
            draw.text((pos_x, pos_y), header, font=bold_font)

            # draw value
            if '^' in value:  # if value too long
                value_parts = value.split('^')
                for day_line in value_parts:
                    draw.text((pos_x + header_offset, pos_y), day_line, font=font)
                    pos_y += y_offset_small
                pos_y += y_offset_small
            else:
                draw.text((pos_x + header_offset, pos_y), value, font=font)
                pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class IsraelHolidaysPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/israel_holidays.png'
        font_size = 50
        title = 'ISRAEL HOLIDAYS TEST'  # TODO title

        self._lines = text.split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 320
        pos_x = 100
        y_offset = 80
        y_offset_small = 60

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        for line in lines:
            # structure: holiday header
            #            date header: date value
            holiday_header = line.split('%')[0]
            date_header, date_value = line.split('%')[1].split('|')
            date_header_offset = font_offset(date_header)

            # draw holiday header
            draw.text((pos_x, pos_y), holiday_header, font=bold_font)
            pos_y += y_offset_small

            # draw date header
            draw.text((pos_x, pos_y), date_header, font=bold_font)

            # draw date value
            draw.text((pos_x + date_header_offset, pos_y), date_value, font=font)
            pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)

# todo set '_' in licalisation file before '|'
