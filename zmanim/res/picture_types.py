from enum import Enum

from zmanim.res.picture_maker import *


class PictureTypes(Enum):
    zmanim = ZmanimPicture
    shabbos = ShabbosPicture
    rosh_chodesh = RoshHodeshPicture
    daf_yomi = DafYomPicture
    rosh_hashana = RoshHashanaPicture
    yom_kippur = YomKippurPicture
    succos = SucosPicture
    shmini_atseres = ShminiAtzeretPicture
    chanukah = ChanukaPicture
    purim = PurimPicture
    pesach = PesahPicture
    shavuos = ShavuotPicture
    tu_bishvat = 13
    lag_baomer = LagBaomerPicture
    israel_holidays = IsraelHolidaysPicture
    fast_gedaliah = FastPicture
    fast_asarah_tevet = FastPicture
    fast_esther = FastPicture
    fast_sheva_asar_tammuz = FastPicture
    fast_tisha_beav = FastPicture
