__all__ = [
    'NoLanguageException',
    'NoLocationException',
    'IncorrectLocationException',
    'IncorrectTextException',
    'IncorrectGregorianDateException',
    'IncorrectJewishDateException',
    'NonUniqueLocatioinException',
    'MaxLocationLimitException'
]


class NoLanguageException(Exception):
    ...


class NoLocationException(Exception):
    ...


class IncorrectLocationException(Exception):
    ...


class IncorrectTextException(Exception):
    ...


class IncorrectGregorianDateException(Exception):
    ...


class IncorrectJewishDateException(Exception):
    ...


class NonUniqueLocatioinException(Exception):
    ...


class MaxLocationLimitException(Exception):
    ...
