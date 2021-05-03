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


class NonUniqueLocationException(Exception):
    ...


class NonUniqueLocationNameException(Exception):
    ...


class MaxLocationLimitException(Exception):
    ...


class ActiveLocationException(Exception):
    ...


KNOWN_EXCEPTIONS = (
    NoLanguageException,
    NoLocationException,
    IncorrectLocationException,
    IncorrectTextException,
    IncorrectGregorianDateException,
    IncorrectJewishDateException,
    NonUniqueLocationException,
    NonUniqueLocationNameException,
    MaxLocationLimitException,
    ActiveLocationException
)
