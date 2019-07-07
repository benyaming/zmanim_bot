from enum import Enum

from zmanim.res.image.picture_maker import *


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
