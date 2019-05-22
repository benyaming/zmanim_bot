from os import path, getcwd
from io import BytesIO
from typing import Callable, NoReturn
from gettext import translation

from PIL import Image, ImageDraw, ImageFont, PngImagePlugin

from ..localizations import *


def get_translator(domain: str, lang: str) -> Callable:
    languages = {'Russian': 'ru', 'English': 'en'}
    loc_path = path.join(path.abspath(getcwd()), 'locales/')
    locale = translation(domain, loc_path, languages=[languages.get(lang)])
    locale.install()
    return locale.gettext


def format_header(header: str) -> str:
    return f'{header}: '


class PictureFactory:

    _font_path = path.join(path.abspath(getcwd()), 'res/image/fonts/gothic.TTF')
    _bold_font_path = path.join(path.abspath(getcwd()), 'res/image/fonts/gothic-bold.TTF')
    _title_font = ImageFont.truetype(_bold_font_path, 60)
    # smaller font for shmini atzeres
    _title_font_sa = ImageFont.truetype(_bold_font_path, 55)
    _bold_font = None

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
                    shmini_atzeres: bool = False) -> None:
        coordinates = (250, 90) if not is_zmanim else (250, 65)
        font = self._title_font if not shmini_atzeres else self._title_font_sa
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


class DafYomPicture(PictureFactory):
    def __init__(self, lang: str, data: dict) -> NoReturn:
        font_size = 90
        background_path = 'res/image/backgrounds/daf_yomi.png'

        self._font = ImageFont.truetype(super()._font_path, font_size)
        self._bold_font = ImageFont.truetype(super()._bold_font_path, font_size)
        self._draw = super()._get_draw(background_path)

        translator = get_translator('daf_yomi', lang)
        localized_data = daf_yomi.get_translate(data, translator)
        self._data = localized_data['data']

        title = localized_data['title']
        self._draw_title(self._draw, title)

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

        for header, value in data.items():
            header = format_header(header)
            header_offset = font_offset(header)

            # draw termin
            draw.text((pos_x, pos_y), f'{header} ', font=bold_font)
            # draw value
            draw.text((pos_x + header_offset, pos_y), value, font=font)

            pos_y += y_offset
        return self._convert_img_to_bytes_io(self._image)


class RoshHodeshPicture(PictureFactory):
    def __init__(self, lang: str, data: dict) -> NoReturn:
        font_size = 46
        background_path = 'res/image/backgrounds/rosh_hodesh.png'

        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)
        self._draw = self._get_draw(background_path)

        translator = get_translator('rosh_hodesh', lang)
        localized_data = rosh_hodesh.get_translate(data, translator)
        self._data = localized_data['data']

        title = localized_data['title']
        self._draw_title(self._draw, title)

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
        month_header = format_header(data['month']['month_word'])
        month_value = data['month']['month_value']
        offset = font_offset(month_header)
        draw.text((pos_x, pos_y), month_header, font=bold_font)
        draw.text((pos_x + offset, pos_y), month_value, font=font)
        pos_y += y_offset

        # draw number of days (nod)
        nod_header = format_header(data['nod']['nod_word'])
        nod_value = data['nod']['nod_value']
        offset = font_offset(nod_header)
        draw.text((pos_x, pos_y), nod_header, font=bold_font)
        draw.text((pos_x + offset, pos_y), str(nod_value), font=font)
        pos_y += y_offset

        # prepare date string
        date = data['date']
        date_str = self.format_rh_date(
            days=date['date_days'],
            months=date['date_months'],
            years=date['date_years'],
            dow=date['date_dow']
        )

        # draw date strings
        date_header = format_header(date['date_word'])
        x_offset = font_offset(date_header)
        optional_y_offset = y_font_offset(date_str) if '\n' in date_str else 0

        draw.text((pos_x, pos_y), date_header, font=bold_font)
        draw.text((pos_x + x_offset, pos_y), date_str, font=font)
        pos_y += y_offset + optional_y_offset
        print(optional_y_offset)

        # prepare molad string
        molad = data['molad']
        molad_str1 = f'{molad["molad_day"]} {molad["molad_month"]}, {molad["molad_dow"]}' \
                     f',\n{molad["molad_n_of_hours"]} {molad["molad_hours_w"]} ' \
                     f'{molad["molad_n_of_minutes"]} {molad["molad_minutes_w"]} ' \
                     f'{molad["molad_and-word"]} {molad["molad_n_of_parts"]} ' \
                     f'{molad["molad_parts_w"]}'

        # draw molad string
        molad_header = format_header(molad['molad_word'])
        offset = font_offset(molad_header)

        draw.text((pos_x, pos_y), molad_header, font=bold_font)
        draw.text((pos_x + offset, pos_y), molad_str1, font=font)

        return self._convert_img_to_bytes_io(self._image)


class ShabbosPicture(PictureFactory):

    def __init__(self, lang: str, data: dict):
        font_size = 60
        warning_font_size = 48

        translator = get_translator('shabbos', lang)
        localized_data = shabbos.get_translate(data, translator)
        self._data = localized_data['data']

        if data['error'] or data['warning']:
            background_path = 'res/image/backgrounds/shabbos_attention.png'
            self._warning = True
        else:
            background_path = 'res/image/backgrounds/shabbos.png'
            self._warning = False

        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)
        self._warning_font = ImageFont.truetype(self._bold_font_path, warning_font_size)
        self._draw = self._get_draw(background_path)

        title = localized_data['title']
        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 400
        pos_x = 100
        y_offset = 80

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        warning_font = self._warning_font
        data = self._data
        draw = self._draw

        # draw parashat hashavua
        p_h = data['parasha']
        header = format_header(p_h['parasha_header'])
        value = p_h['parasha_value']
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), value, font=font)
        pos_y += y_offset

        if data['error']:
            pass

        # draw candle lighting
        c_l = data['candle_lighting']
        header = format_header(c_l['candle_lighting_header'])
        value = c_l['candle_lighting_value']
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), value, font=font)
        pos_y += y_offset

        # draw shekiah offset
        shekiah_offset = data['shkia_offset']

        draw.text((pos_x, pos_y), shekiah_offset, font=font)
        pos_y += y_offset

        # draw tzeis hakochavim
        t_h = data['tzeit_kochavim']
        header = format_header(t_h['tzeit_header'])
        value = t_h['tzeit_value']
        header_offset = font_offset(header)

        draw.text((pos_x, pos_y), header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), value, font=font)
        pos_y += y_offset

        # draw warning if need
        if not data['warning']:
            return self._convert_img_to_bytes_io(self._image)

        warning = data['warning']
        pos_x, pos_y = 100, 840

        draw.text((pos_x, pos_y), warning, font=warning_font, fill='#ff5959')

        # if '%' in text:
        #     text_lines = text.split('%')[0].split('\n')
        # elif '?' in text:
        #     text_lines = text.split('?')[0].split('\n')
        #     pos_y = 470
        # else:
        #     text_lines = text.split('\n')
        #
        # for line in text_lines:
        #     # draw 'candle offset' line without termin offset
        #     if '+' in line:
        #         line = line.split('+')[1]
        #         draw.text((pos_x, pos_y), line, font=font)
        #         pos_y += y_offset
        #     else:
        #         # headers separetes from values by '|' symbol
        #         header, value = line.split('|')
        #         header_offset = font_offset(header)
        #
        #         # draw termin
        #         draw.text((pos_x, pos_y), f'{header} ', font=bold_font)
        #         # draw value
        #         draw.text((pos_x + header_offset, pos_y), value, font=font)
        #         pos_y += y_offset
        #
        # # draw warning message, if it exist
        # warning_lines = ''
        # if '?' in text:
        #     pos_y = 830 if self._lang == 'English' else 810
        #     warning_lines = text.split('?')[1].split('\n')
        # elif '%' in self._text:
        #     warning_lines = text.split('%')[1].split('\n')
        #     pos_y = 830
        # pos_x = 100
        # y_offset = 50
        # for line in warning_lines:
        #     draw.text((pos_x, pos_y), line, font=warning_font, fill='#ff5959')
        #     pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class ZmanimPicture(PictureFactory):

    def _set_font_properties(self, number_of_lines: int) -> None:
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

        font_size, self._y_offset, self._start_y_offset = p.get(number_of_lines)
        self._font = ImageFont.truetype(self._font_path, size=font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, size=font_size)

    def __init__(self, lang, text):
        self._set_font_properties(len(text.split('\n')))

        title = 'ZMANIM TEST'  # TODO title
        background_path = 'res/backgrounds/zmanim.png'

        self._date = text.split('=')[0]
        self._lines = text.split('=')[1].split('\n')
        self._draw = self._get_draw(background_path)

        self._draw_title(self._draw, title, zmanim=True)
        self._draw_date()

    def _draw_date(self):
        pos_x = 250
        pos_y = 80
        draw = self._draw
        date_font = ImageFont.truetype(self._font_path, 40)

        draw.text((pos_x, pos_y + 50), self._date, font=date_font)

    def draw_picture(self):
        pos_y = 210
        pos_x = 100

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        y_offset = self._y_offset
        pos_y += self._start_y_offset

        for line in lines:
            # zman name separates from zman value by `—` symbol
            # todo set default separate symbol ('|')
            zman, value = line.split('—')
            zman_offset = font_offset(zman)

            # draw zman name
            draw.text((pos_x, pos_y), zman, font=bold_font)

            # draw zman value
            draw.text((pos_x + zman_offset, pos_y), value, font=font)
            pos_y += y_offset
        return self._convert_img_to_bytes_io(self._image)


class FastPicture(PictureFactory):

    def __init__(self, lang, text):
        title = text.split('\n\n')[0]
        background_path = 'res/backgrounds/fast.png'
        font_size = 60

        self._lines = text.split('\n\n')[1].split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 290
        pos_x = 100
        y_offset = 80

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        for line in lines:
            # separate the fast's end block
            if line.startswith('%'):
                line = line.split('%')[1]
                pos_y += y_offset

            # separate the chatzot
            if line.startswith('$'):
                line = line.split('$')[1]
                pos_y += 40

            # headers separetes from values by '|' symbol
            header, value = line.split('|')
            header_offset = font_offset(header)

            # draw header
            draw.text((pos_x, pos_y), header, font=bold_font)

            # draw value in miltiple lines
            for value_part in value.split('^'):
                draw.text((pos_x + header_offset, pos_y), value_part, font=font)
                if '^' in line:
                    pos_y += y_offset - 15
                else:
                    pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class RoshHashanaPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/rosh_hashana.png'
        font_size = 50
        title = 'ROSH HASHANAH TEST'  # TODO title

        self._lines = text.split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 300
        pos_x = 100
        y_offset = 75
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
            if '^' in value:  # if value is too long for one string
                # TODO try: `for x in value.split('^')`
                day_lines = value.split('^')
                for day_line in day_lines:
                    draw.text((pos_x + header_offset, pos_y), day_line, font=font)
                    pos_y += y_offset_small
                pos_y += y_offset_small
            else:
                draw.text((pos_x + header_offset, pos_y), value, font=font)
                pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class YomKippurPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/yom_kippur.png'
        font_size = 60
        title = text.split('\n\n')[0]

        self._draw = self._get_draw(background_path)
        self._lines = text.split('\n\n')[1].split('\n')
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 300
        pos_x = 100
        y_offset = 120
        y_offset_small = 60

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        # due to non-standart structure of this picture let's draw it manually
        # lines structure: [date, candle_lighting, havdalah]

        # draw date
        date_header = lines[0].split('|')[0]
        date, day_of_week = lines[0].split('|')[1].split('^')
        header_offset = font_offset(date_header)

        draw.text((pos_x, pos_y), date_header, font=bold_font)
        draw.text((pos_x + header_offset, pos_y), date, font=font)
        pos_y += y_offset_small
        draw.text((pos_x + header_offset, pos_y), day_of_week, font=font)
        pos_y += y_offset

        # draw candle ligting (with two-lines header)
        cl_header1, cl_header2 = lines[1].split('%')[0].split('?')
        cl_time = lines[1].split('%')[1]

        draw.text((pos_x, pos_y), cl_header1, font=bold_font)
        pos_y += y_offset_small
        draw.text((pos_x, pos_y), cl_header2, font=bold_font)
        pos_y += y_offset_small
        draw.text((pos_x, pos_y), cl_time, font=font)
        pos_y += y_offset

        # draw havdalah
        havdalah_header, havdala_time = lines[2].split('%')
        draw.text((pos_x, pos_y), havdalah_header, font=bold_font)
        pos_y += y_offset_small
        draw.text((pos_x, pos_y), havdala_time, font=font)

        return self._convert_img_to_bytes_io(self._image)


class SucosPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/succos.png'
        font_size = 50
        title = 'SUCCOS TEST'  # TODO title

        self._lines = text.split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 300
        pos_x = 100
        y_offset = 75
        y_offset_small = 65

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        # draw succos data
        for line in lines:
            # headers separetes from values by '|' symbol
            header, value = line.split('|')
            header_offset = font_offset(header)

            # draw header
            draw.text((pos_x, pos_y), header, bold_font)

            # draw value in multiple lines
            value_parts = value.split('^')
            first_iteration = True
            for value_part in value_parts:
                if not first_iteration:
                    pos_y += y_offset_small
                draw.text((pos_x + header_offset, pos_y), value_part, font=font)
                first_iteration = False
            pos_y += y_offset

        return self._convert_img_to_bytes_io(self._image)


class ShminiAtzeretPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/shmini_atzeret.png'
        font_size = 45
        title = 'SHMINI TEST'  # TODO title

        self._lines = text.split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title, shmini_atzeres=True)

    def draw_image(self):
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

            if '^' in value:  # draw value in multiple lines
                day_lines = value.split('^')
                for day_line in day_lines:
                    draw.text((pos_x + header_offset, pos_y), day_line, font=font)
                    pos_y += y_offset_small
                pos_y += y_offset_small
            else:  # draw value in single line
                draw.text((pos_x + header_offset, pos_y), value, font=font)
                pos_y += y_offset

        self._convert_img_to_bytes_io(self._image)


class ChanukaPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/chanuka.png'
        title = 'CHANUKKAH TEST'  # TODO title
        font_size = 60

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


class TuBiShvatPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/tubishvat.png'
        font_size = 70
        title = 'TU BISHVAT TEST'  # TODO title

        self._lines = text.split('\n')
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
        text = self._lines
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


class PurimPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/purim.png'
        font_size = 70
        title = 'PURIM TEST'  # TODO title

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


class PesahPicture(PictureFactory):

    def __init__(self, lang, text):
        background_path = 'res/backgrounds/pesah.png'
        font_size = 43 if lang == 'English' or '(' not in text else 50
        title = 'PESACH TEST'  # TODO title

        self._lines = text.split('\n')
        self._draw = self._get_draw(background_path)
        self._font = ImageFont.truetype(self._font_path, font_size)
        self._bold_font = ImageFont.truetype(self._bold_font_path, font_size)

        self._draw_title(self._draw, title)

    def draw_picture(self):
        pos_y = 270
        pos_x = 100
        y_offset = 65
        y_offset_small = 65

        # shortcuts for code glance
        font_offset = self._font_offset
        font = self._font
        bold_font = self._bold_font
        lines = self._lines
        draw = self._draw

        # draw pesah data
        for line in lines:
            # headers separetes from values by '|' symbol
            header, value = line.split('|')
            header_offset = font_offset(header)

            if '!' in header:
                pos_y += y_offset_small
                header = header.replace('!', '')

            # draw header
            draw.text((pos_x, pos_y), header, font=bold_font)

            # draw value
            value_parts = value.split('^')
            first_iteration = True

            for value_part in value_parts:
                if not first_iteration:
                    pos_y += y_offset_small
                draw.text((pos_x + header_offset, pos_y), value_part, font=font)
                first_iteration = False
            pos_y += y_offset

        self._convert_img_to_bytes_io(self._image)


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
