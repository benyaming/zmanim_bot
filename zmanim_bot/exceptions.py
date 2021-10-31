# KNOWN_EXCEPTIONS = []


class ZmanimBotBaseException(Exception):
    ...
    # def __init_subclass__(cls, **kwargs):
    #     KNOWN_EXCEPTIONS.append(cls)


class NoLanguageException(ZmanimBotBaseException):
    ...


class NoLocationException(ZmanimBotBaseException):
    ...


class IncorrectLocationException(ZmanimBotBaseException):
    ...


class IncorrectTextException(ZmanimBotBaseException):
    ...


class IncorrectGregorianDateException(ZmanimBotBaseException):
    ...


class IncorrectJewishDateException(ZmanimBotBaseException):
    ...


class NonUniqueLocationException(ZmanimBotBaseException):
    ...


class NonUniqueLocationNameException(ZmanimBotBaseException):
    ...


class MaxLocationLimitException(ZmanimBotBaseException):
    ...


class ActiveLocationException(ZmanimBotBaseException):
    ...


class PolarCoordinatesException(ZmanimBotBaseException):
    ...


class UnknownProcessorException(ZmanimBotBaseException):
    ...
