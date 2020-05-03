import asyncio

from aiogram import Bot
from aiogram.types import ChatActions

from zmanim_bot import texts
from .helpers import UserDataTypes
from . import keyboards, config
from zmanim_bot.api import _public


class TextHandler:

    @property
    async def lang(self):
        if not self.__lang:
            return await _public.get_user_data(self.user_id, UserDataTypes.lang)
        return self.__lang

    @property
    async def location(self):
        if not self.__location:
            return await _public.get_user_data(self.user_id, UserDataTypes.location)
        return self.__location

    def __init__(self, user_id: int, text: str = None):
        self.user_id = user_id
        self.text = text
        self.bot = Bot.get_current()
        self.__lang = None
        self.__location = None

    async def process_text(self):
        """Coro for handling and processing user's messages"""
        # if state
        if self.text in config.LANGUAGE_LIST:

            self.__lang = self.text
            asyncio.create_task(self._set_lang())
            return await self.main_menu()

        # handler = self._commands.get(self.text, self._incorrect_text)
        # if self.text in self._commands:  # todo better
        #     handler = self._commands.get(self.text, self._incorrect_text)
        # else:
        #     handler = TextHandler._incorrect_text
        # await handler(self)

    ###############################################################################
    #                                 MENUS                                       #
    ###############################################################################

    async def main_menu(self):
        kb = keyboards.get_main_menu(await self.lang)
        resp = texts.mm_welcome
        await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #
    # async def _help_menu(self):
    #     """Sends help menu to user"""
    #     # self._chatbase('help', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     resp = texts.hm_welcome
    #     kb = keyboards.get_help_menu(self.lang)
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open help menu')
    #
    # async def _settings_menu(self):
    #     """Sends settings menu to user"""
    #     # self._chatbase('settings menu', 'user')
    #     kb = keyboards.get_settings_menu(self.lang)
    #     resp = texts.sm_welcome
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open settings menu')
    #
    # async def _holidays_menu(self):
    #     """Sends holidays menu to user"""
    #     # self._chatbase('holidays menu', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     resp = texts.hom_welcome
    #     kb = keyboards.get_holidays_menu(self.lang)
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open holidays menu')
    #
    # async def _more_holiday_menu(self):
    #     """Sends additional holidays menu to user"""
    #     # self._chatbase('more holidays menu', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     kb = keyboards.get_more_holidays_menu(self.lang)
    #     resp = texts.hom_welcome
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open more holidays menu')
    #
    # async def _fasts_menu(self):
    #     """Sends fasts menu to user"""
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     # self._chatbase('holidays menu', 'user')
    #     resp = texts.hm_welcome
    #     kb = keyboards.get_fast_menu(self.lang)
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open fasts menu')

    ###############################################################################
    #                                HELPERS                                      #
    ###############################################################################

    # async def _incorrect_text(self):
    #     """
    #     If user send text not from keyboard or method for this text not implemented yet:
    #     """
    #     resp = texts.incorrect_text
    #     await self.bot.send_message(self.user_id, resp)
    #     await self._main_menu()
    #
    # async def _report(self):
    #     """
    #     When user wants to report a bug, he writes a message and the bot redirects it
    #     to admin.
    #     """
    #     # self._chatbase('report', 'user')
    #     # todo send cancel keyboard
    #     # todo report function
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     resp = texts.report
    #     await self.bot.send_message(self.user_id, resp, disable_web_page_preview=True)
    #     # self._chatbase('report message sent')
    #
    # async def _faq(self):
    #     """Sends link to FAQ page to user"""
    #     # self._chatbase('faq', 'user')
    #     faq_links = {  # TODO as translated text?
    #         'Russian': 'http://telegra.ph/Hebrew-Calendar-Bot-FAQ-05-10',
    #         'English': 'http://telegra.ph/Hebrew-Calendar-Bot-FAQ-EN-05-10'
    #     }
    #     resp = faq_links.get(self.lang, 'no language selected')
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('faq sent')

    ###############################################################################
    #                               LANGUAGE                                      #
    ###############################################################################

    # async def _change_lang(self):
    #     """
    #     When user wants to change language, bot sends him a keyboard with languages
    #     """
    #     # self._chatbase('change lang', 'user')
    #     resp = 'Выберите язык/Choose the language'
    #     kb = keyboards.get_lang_menu()
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open language menu')
    #

    async def _set_lang(self):
        self.__lang = self.text
        await _public.set_user_data(self.user_id, UserDataTypes.lang, self.__lang)

    ###############################################################################
    #                               LOCATION                                      #
    ###############################################################################

    async def request_location(self):
        await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
        kb = keyboards.get_geobutton(await self.lang)
        resp = texts.request_location
        await self.bot.send_message(self.user_id, resp, reply_markup=kb)
        # self._chatbase('request location')

    # async def _update_location(self):
    #     """
    #     Same as `_request_location`, but with 'Cancel' button. Used for case when user
    #     has already location.
    #     """
    #     # self._chatbase('update location', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     kb = keyboards.get_geobutton(self.lang, True)
    #     resp = texts.request_location
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open menu update location')
    #
    # ###############################################################################
    # #                               SETTINGS                                      #
    # ###############################################################################
    #
    # async def _select_zmanim(self):
    #     """
    #     Zmanim selection menu. Sends to user inline keyboard with zmanim switchers.
    #     """
    #     # self._chatbase('select zmanim', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     kb = None  # todo zmanim inline kb
    #     resp = 'here will zmanim options'  # todo txt
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open zmanim options')
    #
    # async def _select_candle_offset(self):
    #     """
    #     Candle lighting offset menu. Sends to user inline keyboard with offset switchers.
    #     """
    #     # self._chatbase('select candle offset', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     kb = None  # todo cl kb
    #     resp = 'here will cl options'  # todo txt
    #     await self.bot.send_message(self.user_id, resp, reply_markup=kb)
    #     # self._chatbase('open candle offset options')

    ###############################################################################
    #                          MAIN MENU FUNCTIONS                                #
    ###############################################################################

    # async def _get_zmanim(self):
    #     """Sends to user zmanim picture"""
    #     # self._chatbase('zmanim', 'user')
    #     resp = 'here will zmanim'  # todo zmanim, errors
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('zmanim sent')
    #
    # def _get_zmanim_by_the_date(self, day: int, month: int, year: int):
    #     """Sends to user zmanim by the date picture"""
    #     # todo zmanim by the date
    #     # todo errors
    #     # todo delete state
    #     custom_date = (year, month, day)
    #     resp = 'here will zmanim by the date'
    #     self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('zmanim by the date sent')
    #     self._main_menu()
    #
    # async def _shabbat(self):
    #     """Sends to user Shabbos picture"""
    #     # self._chatbase('shabbos', 'user')
    #     # todo shabbos
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'here will shabbos'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('shabbos sent')
    #
    # async def _rosh_chodesh(self):
    #     """Sends to user Rosh hodesh picture"""
    #     # self._chatbase('rosh chodesh', 'user')
    #     # todo rosh hodesh
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'here will rosh hodesh'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('rosh chodesh sent')
    #
    # async def _daf_yomi(self) -> None:
    #     """Sends to user Daf yomi pictire"""
    #     # self._chatbase('daf yomi', 'user')
    #     # todo daf yomi
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'here will daf yomi'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('daf yomi sent')
    #
    # ###############################################################################
    # #                                CONVERTER                                    #
    # ###############################################################################
    #
    # # @check_auth
    # # def _converter_startup(self):
    # #     self._chatbase('converter', 'user')
    # #     self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    # #     resp = locale.Converter.welcome_to_converter(self.lang)
    # #     markup = kbrd.get_converter_menu(self.lang)
    # #     self.bot.send_message(self.user_id, resp, reply_markup=markup)
    # #     self._chatbase('open converter menu')
    # #
    # # @check_auth
    # # def _converter_greg_to_heb(self):
    # #     self._chatbase('convert greg -> heb', 'user')
    # #     self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    # #     states.set_state(self.user_id, 'waiting_for_greg_date')
    # #     resp = locale.Converter.request_date_for_converter_greg(self.lang)
    # #     keyboard = kbrd.get_cancel_keyboard(self.lang)
    # #     self.bot.send_message(
    # #         self.user_id,
    # #         resp,
    # #         parse_mode='Markdown',
    # #         reply_markup=keyboard
    # #     )
    # #     self._chatbase('ask for date to convert')
    # #
    # # @check_auth
    # # def _convert_heb_to_greg(self):
    # #     self._chatbase('convert heb -> greg', 'user')
    # #     self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    # #     states.set_state(self.user_id, 'waiting_for_heb_date')
    # #     resp = locale.Converter.request_date_for_converter_heb(self.lang)
    # #     keyboard = kbrd.get_cancel_keyboard(self.lang)
    # #     self.bot.send_message(
    # #         self.user_id,
    # #         resp,
    # #         parse_mode='Markdown',
    # #         reply_markup=keyboard
    # #     )
    # #     self._chatbase('ask for date to convert')
    #
    # ###############################################################################
    # #                             HANDLING DATES                                  #
    # ###############################################################################
    # # todo date validators in another module
    # # @check_auth
    # # def _request_date(self):
    # #     self._chatbase('zmanim by the date', 'user')
    # #     self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    # #     states.set_state(self.user_id, 'waiting_for_date')
    # #     resp = locale.Utils.request_date(self.lang)
    # #     keyboard = kbrd.get_cancel_keyboard(self.lang)
    # #     self.bot.send_message(
    # #         self.user_id,
    # #         resp,
    # #         parse_mode='Markdown',
    # #         reply_markup=keyboard
    # #     )
    # #     self._chatbase('request date for zmanim sent')
    # #
    # def _handle_date(self):
    #     self._chatbase('received custom date', 'user')
    #     reg_pattern = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
    #     extracted_date = re.search(reg_pattern, self._text)
    #     if extracted_date:
    #         day = int(extracted_date.group().split('.')[0])
    #         month = int(extracted_date.group().split('.')[1])
    #         year = int(extracted_date.group().split('.')[2])
    #         try:
    #             datetime(year, month, day)
    #             self._get_zmanim_by_the_date(day, month, year)
    #         except ValueError:
    #             self._incorrect_date('incorrect_date_value')
    #             self._chatbase('incorrect date value')
    #     else:
    #         self._incorrect_date('incorrect_date_format')
    #         self._chatbase('incorrect date format')
    #
    # def _handle_greg_date(self):
    #     self._chatbase('handle greg date', 'user')
    #     self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    #     reg_pattern = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4}$'
    #     extracted_date = re.search(reg_pattern, self._text)
    #     if extracted_date:
    #         day = int(extracted_date.group().split('.')[0])
    #         month = int(extracted_date.group().split('.')[1])
    #         year = int(extracted_date.group().split('.')[2])
    #         try:
    #             datetime(year, month, day)
    #             date = (year, month, day)
    #             resp = conv.convert_greg_to_heb(date, self.lang)
    #             keyboard = kbrd.get_zmanim_for_converter_button(
    #                 date,
    #                 self.lang
    #             )
    #             self.bot.send_message(
    #                 self.user_id,
    #                 resp,
    #                 parse_mode='Markdown',
    #                 reply_markup=keyboard
    #             )
    #             states.delete_state(self.user_id)
    #             self._chatbase('greg date converted')
    #             self._main_menu()
    #         except Exception:
    #             self._incorrect_date('incorrect_date_value')
    #             self._chatbase('incorrect date value')
    #     else:
    #         self._incorrect_date('incorrect_date_format')
    #         self._chatbase('incorrect date format')
    #
    # def _handle_heb_date(self):
    #     input_data = self._text.split()
    #     if len(input_data) in [3, 4]:
    #         # check day
    #         if input_data[0].isdigit():
    #             '''check day'''
    #         # check month
    #         if len(input_data) == 3:
    #             # all exept adar ii
    #             if input_data[1].lower() in data.heb_months_names_ru:
    #                 '''check month'''
    #         elif len(input_data) == 4:
    #             '''check month'''
    #         else:
    #             return self._incorrect_date('incorrect_heb_date_format')
    #         # check year
    #         if input_data[-1].isdigit():
    #             year = int(input_data[-1])
    #             if year < 0:
    #                 return self._incorrect_date('incorrect_heb_date_value')
    #             # final calculation
    #             else:
    #                 hebrew_date = (year, month, day)
    #                 resp = conv.convert_heb_to_greg(hebrew_date, self.lang)
    #                 if resp:
    #                     message_text = resp['resp']
    #                     if type(resp['date']) == list:
    #                         keyboard = kbrd.get_zmanim_for_two_addars(resp['date'], self.lang)
    #                     else:
    #                         keyboard = kbrd.get_zmanim_for_converter_button(resp['date'], self.lang)
    #                     self.bot.send_message(self.user_id, message_text, parse_mode='Markdown', reply_markup=keyboard)
    #                     states.delete_state(self.user_id)
    #                     self._chatbase('heb date converted')
    #                     self._main_menu()
    #                 else:
    #                     self._chatbase('incorrect date value')
    #                     return self._incorrect_date('incorrect_heb_date_value')
    #     else:
    #         self._chatbase('incorrect date format')
    #         return self._incorrect_date('incorrect_heb_date_format')
    # #
    # # def _incorrect_date(self, error_type: str) -> None:
    # #     self.bot.send_chat_action(self.user_id, ChatActions.TYPING)
    # #     resps = {
    # #         'incorrect_date_format': locale.Utils.incorrect_date_format(
    # #             self.lang
    # #         ),
    # #         'incorrect_date_value': locale.Utils.incorrect_date_value(
    # #             self.lang
    # #         ),
    # #         'incorrect_heb_date_format':
    # #             locale.Converter.incorrect_heb_date_format(self.lang),
    # #         'incorrect_heb_date_value':
    # #             locale.Converter.incorrect_heb_date_value(self.lang)
    # #     }
    # #     resp = resps.get(error_type, '')
    # #     keyboard = kbrd.get_cancel_keyboard(self.lang)
    # #     self.bot.send_message(
    # #         self.user_id,
    # #         resp,
    # #         parse_mode='Markdown',
    # #         reply_markup=keyboard
    # #     )
    # #
    #
    # ###############################################################################
    # #                             HANDLING USER INPUT                             #
    # ###############################################################################
    #
    # ###############################################################################
    # #                                   HOLIDAYS                                  #
    # ###############################################################################
    #
    # async def _rosh_hashana(self):
    #     """Sends Rosh hashana picture to user"""
    #     # todo request
    #     # todo picture
    #     # self._chatbase('rosh hashana', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'rosh hashana'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('rosh hashana sent')
    #
    # async def _yom_kippur(self):
    #     """Sends Yom kippur picture to user"""
    #     # todo request
    #     # todo pictire
    #     # self._chatbase('yom kippur', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'yom kippur'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('yom kippur sent')
    #
    # async def _succot(self):
    #     """Sends Succos picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('succos', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'succos'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('succos sent')
    #
    # async def _shmini_atzeret(self):
    #     """Sends Shmini atzeres picture to user"""
    #     # todo request
    #     # todo picture
    #     # self._chatbase('shmini atzeres', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'shmini atzeres'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('shmini atzeres sent')
    #
    # async def _chanukah(self):
    #     """Sends Chanukah picture to user"""
    #     # self._chatbase('chanukah', 'user')
    #     # todo request
    #     # todo img
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'chanukah'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('chanukah sent')
    #
    # async def _tu_bishvat(self):
    #     """Sends Tu bi-shvat picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('tu bishvat', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'tu bishvat'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('tu bishvat sent')
    #
    # async def _purim(self):
    #     """Sends Purim picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('purim', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'purim'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('purim sent')
    #
    # async def _pesach(self):
    #     """Sends Pesach picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('pesach', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'pesach'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('pesach sent')
    #
    # async def _lag_baomer(self):
    #     """Sends Lag ba-omer picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('lag baomer', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'lag baomer'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('lag baomer sent')
    #
    # async def _shavuos(self):
    #     """Sends Shavuos picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('shavuos', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'shavuos'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('shavuos sent')
    #
    # async def _israel_holidays(self):
    #     """Sends Israel holidays picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('israel', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'israel holidays'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('israel sent')
    #
    # ###############################################################################
    # #                                 FASTS                                       #
    # ###############################################################################
    #
    # async def _fast_gedaliah(self):
    #     """Sends Fast of Gedalia picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('fast gedaliah', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'fast gedaliah'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('fast gedaliah sent')
    #
    # async def _asarah_betevet(self):
    #     """Sends Fast of 10th of Teveth picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('10 of tevet', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = '10 tevet'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('10 of tevet sent')
    #
    # async def _fast_esther(self):
    #     """Sends Fast of Esther picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('fast esther', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = 'fast esther'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('fast esther sent')
    #
    # async def _sheva_asar_betammuz(self):
    #     """Sends Fast of 17th of Tammuz picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('17 of tammuz', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = '17 tammuz'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('17 of tammuz sent')
    #
    # async def _tisha_beav(self):
    #     """Sends Fast of 9th of Av picture to user"""
    #     # todo request
    #     # todo img
    #     # self._chatbase('9 of av', 'user')
    #     await self.bot.send_chat_action(self.user_id, ChatActions.UPLOAD_PHOTO)
    #     resp = '9 av'
    #     await self.bot.send_message(self.user_id, resp)
    #     # self._chatbase('9 of av sent')
    #
    # _commands = {
    #     'Язык': _change_lang,
    #     'Language': _change_lang,
    #     'Отмена': _main_menu,
    #     'Cancel': _main_menu,
    #     'Русский': _setlang,
    #     'English': _setlang,
    #     'Hebrew': _setlang,
    #     'Назад/Back': _change_lang,
    #     'Зманим': _get_zmanim,
    #     'Zmanim': _get_zmanim,
    #     # 'Зманим по дате': _request_date,
    #     # 'Zmanim by the date': _request_date,
    #     'Шаббат': _shabbat,
    #     'Shabbos': _shabbat,
    #     'Рош ходеш': _rosh_chodesh,
    #     'Rosh chodesh': _rosh_chodesh,
    #     'Праздники': _holidays_menu,
    #     'Holidays': _holidays_menu,
    #     'Посты': _fasts_menu,
    #     'Fast days': _fasts_menu,
    #     'Даф йоми': _daf_yomi,
    #     'Daf yomi': _daf_yomi,
    #     'Местоположение': _update_location,
    #     'Location': _update_location,
    #     'Назад': _main_menu,
    #     'Back': _main_menu,
    #     'ЧаВо': _faq,
    #     'F.A.Q.': _faq,
    #     '🇷🇺': _faq,
    #     '🇱🇷': _faq,
    #     'Ещё...': _more_holiday_menu,
    #     'More...': _more_holiday_menu,
    #     'Основные праздники': _holidays_menu,
    #     'Main holidays': _holidays_menu,
    #     'Main menu': _main_menu,
    #     'Главное меню': _main_menu,
    #     'Рош а-шана': _rosh_hashana,
    #     'Rosh ha-shanah': _rosh_hashana,
    #     'Йом кипур': _yom_kippur,
    #     'Yom kippur': _yom_kippur,
    #     'Суккот': _succot,
    #     'Succos': _succot,
    #     'Шмини ацерет': _shmini_atzeret,
    #     'Shmini atzeres': _shmini_atzeret,
    #     'Ханука': _chanukah,
    #     'Chanukah': _chanukah,
    #     'Ту би-Шват': _tu_bishvat,
    #     'Tu bi-Shvat': _tu_bishvat,
    #     'Пурим': _purim,
    #     'Purim': _purim,
    #     'Пейсах': _pesach,
    #     'Pesach': _pesach,
    #     'Лаг ба-омер': _lag_baomer,
    #     'Lag ba-omer': _lag_baomer,
    #     'Шавуот': _shavuos,
    #     'Shavuos': _shavuos,
    #     'Израильские праздники': _israel_holidays,
    #     'Israel holidays': _israel_holidays,
    #     'Пост Гедалии': _fast_gedaliah,
    #     'Fast of Gedaliah': _fast_gedaliah,
    #     '10 Тевета': _asarah_betevet,
    #     '10 of Tevet': _asarah_betevet,
    #     'Пост Эстер': _fast_esther,
    #     'Fast of Esther': _fast_esther,
    #     '17 Таммуза': _sheva_asar_betammuz,
    #     '17 of Tammuz': _sheva_asar_betammuz,
    #     '9 Ава': _tisha_beav,
    #     '9 of Av': _tisha_beav,
    #     'Настройки': _settings_menu,
    #     'Settings': _settings_menu,
    #     'Выбрать зманим': _select_zmanim,
    #     'Select zmanim': _select_zmanim,
    #     'Зажигание свечей': _select_candle_offset,
    #     'Candle lighting': _select_candle_offset,
    #     # 'Конвертер дат': _converter_startup,
    #     # 'Date converter': _converter_startup,
    #     # 'Григорианский ➡️ Еврейский': _converter_greg_to_heb,
    #     # 'Gregorian ➡️ Hebrew': _converter_greg_to_heb,
    #     # 'Еврейский ➡️ Григорианский': _convert_heb_to_greg,
    #     # 'Hebrew ➡️ Gregorian': _convert_heb_to_greg,
    #     'Помощь': _help_menu,
    #     'Help': _help_menu,
    #     'Сообщить об ошибке': _report,
    #     'Report a bug': _report,
    #     'Локация': _update_location
    # }
