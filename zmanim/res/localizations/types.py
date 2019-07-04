from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class SimpleDict:
    """
    A simple dict {'header': str, 'value': str}
    """
    header: str
    value: str


@dataclass
class GenericYomTovData:
    """
    A data class for yom tov with required first day and optional second day and shabbos
    """
    date: SimpleDict
    cl_1: SimpleDict
    cl_2: Optional[SimpleDict]
    cl_3: Optional[SimpleDict]
    havdala: SimpleDict


@dataclass
class GenericYomTov:
    title: str
    data: GenericYomTovData

# -------------- DAF YOMI DATA CLASSES -------------- #


@dataclass
class DYData:
    masehet: SimpleDict
    daf: SimpleDict


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
    month: SimpleDict
    n_days: SimpleDict
    date: RHDate
    molad: RHMolad


@dataclass
class RoshHodesh:
    title: str
    data: RHData

# -------------- SHABBOS DATA CLASSES -------------- #


@dataclass
class ShabosData:
    parasha: SimpleDict
    candle_lighting: Optional[SimpleDict]
    shkia_offset: Optional[str]
    tzeit_kochavim: Optional[SimpleDict]
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
    start_time: SimpleDict
    tzeit_kochavim: SimpleDict
    sba_time: SimpleDict
    nvr_time: SimpleDict
    ssk_time: SimpleDict
    hatzot: Optional[SimpleDict]


@dataclass
class Fast:
    title: str
    data: FastData


# -------------- YOM KIPPUR DATA CLASSES -------------- #

@dataclass
class YomKippurData:
    date: SimpleDict
    candle_lighting: SimpleDict
    havdala: SimpleDict


@dataclass
class YomKippur:
    title: str
    data: YomKippurData


# -------------- SUCCOS DATA CLASSES -------------- #

@dataclass
class SuccosData:
    date: SimpleDict
    candle_lighting_1: SimpleDict
    candle_lighting_2: Optional[SimpleDict]
    candle_lighting_3: Optional[SimpleDict]
    havdala: SimpleDict
    hoshana_raba: SimpleDict


@dataclass
class Succos:
    title: str
    data: SuccosData

# -------------- SHMINI ATZERES DATA CLASSES -------------- #

