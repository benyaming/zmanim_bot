__all__ = [
    'NoLanguageException',
    'NoLocationException',
    'IncorrectLocationException',
    'IncorrectTextException',
    'IncorrectGregorianDateException',
    'IncorrectJewishDateException',
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

