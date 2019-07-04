from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class GenericData:
    """
    A simple data struct like {'header': str, 'value': str}
    """
    header: str
    value: str


@dataclass
class GenericYomTovData:
    """
    A data class for yom tov with required first day and optional second day and shabbos
    """
    cl_1: GenericData
    cl_2: Optional[GenericData]
    cl_3: Optional[GenericData]
    havdala: GenericData
    date: Optional[GenericData] = None


@dataclass
class GenericYomTov:
    title: str
    data: GenericYomTovData


@dataclass
class GenericHoliday:
    title: str
    date: GenericData

# -------------- DAF YOMI DATA CLASSES -------------- #


@dataclass
class DYData:
    masehet: GenericData
    daf: GenericData


@dataclass
class DafYomi:
    title: str
    data: DYData

# -------------- ROSH HODESH DATA CLASSES -------------- #


@dataclass
class RHDate:
    header: str
    days: List[str]
    months: List[str]
    years: List[str]
    dow: List[str]


@dataclass
class RHMolad:
    header: str
    day: str
    month: str
    dow: str
    n_hours: str
    hours_word: str
    n_of_minutes: str
    minutes_word: str
    and_word: str
    n_parts: str
    parts_word: str


@dataclass
class RHData:
    month: GenericData
    n_days: GenericData
    date: RHDate
    molad: RHMolad


@dataclass
class RoshHodesh:
    title: str
    data: RHData

# -------------- SHABBOS DATA CLASSES -------------- #


@dataclass
class ShabosData:
    parasha: GenericData
    candle_lighting: Optional[GenericData]
    shkia_offset: Optional[str]
    tzeit_kochavim: Optional[GenericData]
    warning: Optional[str]
    error: Optional[str]


@dataclass
class Shabos:
    title: str
    data: ShabosData


# -------------- ZMANIM DATA CLASSES -------------- #


@dataclass
class Zmanim:
    title: str
    date: str
    zmanim: Dict[str, str]

# -------------- FAST DATA CLASSES -------------- #


@dataclass
class FastData:
    start_time: GenericData
    tzeit_kochavim: GenericData
    sba_time: GenericData
    nvr_time: GenericData
    ssk_time: GenericData
    hatzot: Optional[GenericData]


@dataclass
class Fast:
    title: str
    data: FastData


# -------------- YOM KIPPUR DATA CLASSES -------------- #

@dataclass
class YomKippurData:
    date: GenericData
    candle_lighting: GenericData
    havdala: GenericData


@dataclass
class YomKippur:
    title: str
    data: YomKippurData


# -------------- SUCCOS DATA CLASSES -------------- #

@dataclass
class SuccosData:
    date: GenericData
    candle_lighting_1: GenericData
    candle_lighting_2: Optional[GenericData]
    candle_lighting_3: Optional[GenericData]
    havdala: GenericData
    hoshana_raba: GenericData


@dataclass
class Succos:
    title: str
    data: SuccosData


# -------------- PESACH DATA CLASSES -------------- #
@dataclass
class PesachData:
    date: GenericData
    part_1: GenericYomTovData
    part_2: GenericYomTovData


@dataclass
class Pesach:
    title: str
    data: PesachData

