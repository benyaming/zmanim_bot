from enum import Enum


class TriggerType(Enum):
    gregorian_date = 'gregorian_date'
    hebrew_date = 'hebrew_date'
    zman = 'zman'


class ZmanType(Enum):
    alos = 'alos'
    misheyakir_10_2 = 'misheyakir_10_2'
    sunrise = 'sunrise'
    sof_zman_shema_ma = 'sof_zman_shema_ma'
    sof_zman_shema_gra = 'sof_zman_shema_gra'
    sof_zman_tefila_ma = 'sof_zman_tefila_ma'
    sof_zman_tefila_gra = 'sof_zman_tefila_gra'
    chatzos = 'chatzos'
    mincha_gedola = 'mincha_gedola'
    mincha_ketana = 'mincha_ketana'
    plag_mincha = 'plag_mincha'
    sunset = 'sunset'
    tzeis_5_95_degrees = 'tzeis_5_95_degrees'
    tzeis_8_5_degrees = 'tzeis_8_5_degrees'
    tzeis_42_minutes = 'tzeis_42_minutes'
    tzeis_72_minutes = 'tzeis_72_minutes'
    chatzot_laila = 'chatzot_laila'





