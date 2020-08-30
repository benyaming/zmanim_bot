import logging
import sys
from json import dumps
from types import TracebackType
from typing import Any

from better_exceptions.better_exceptions import ExceptionFormatter

LOG_FORMAT = '%(asctime)-15s [ %(levelname)s ] <|> %(message)s'
DATETIME_FORMAT = '%d-%m-%Y > %H:%M:%S'


NEW_LOG_FORMAT = '{asctime} {levelname} {thread} --- [{threadName}] {module}.{funcName}       : {message}'
NEW_DATE_FORMAT = '%d-%m-%Y %H:%M:%S'


UVICORN_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': 'MyFormatter'
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'format': '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
        }
    },
    'handlers': {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'access': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'uvicorn.error': {
            'level': 'DEBUG',
            'handlers': ['default'],
            'propagate': False
        },
        'uvicorn.access': {
            'level': 'DEBUG',
            'handlers': ['access'],
            'propagate': False
        }
    }
}


def _get_detailed_traceback(exc_info: TracebackType):
    exc_type, exc_value, exc_tb = exc_info
    lines = list(ExceptionFormatter(colorize=True).format_exception(exc_type, exc_value, exc_tb))
    return ''.join(lines)


def _shorter_log_record(text: Any) -> str:
    if len(str(text)) > 3000:
        prefix = 'Log record is too long. Here is truncated version:'
        if isinstance(text, (list, dict, tuple, set)):
            elems = []
            for elem in text:
                if isinstance(elem, dict):
                    key = list(filter(lambda e: e.lower() in ['id', 'uuid', 'uu_id'], elem))
                    if len(key) > 0:
                        elems.append(f'{elem[key[0]]}...')
                elif isinstance(elem, list):
                    elems = [elem[0], elem[1], '...']
                else:
                    elems.append(str(elem)[:25])

            if len(elems) > 30:
                elems = elems[:30]
                elems.append('...')

            msg = f'{dumps(elems, indent=2)}\n'
        else:
            msg = f'{str(text)[:1000]}...\n'
        resp = f'{prefix}\n{msg}'
    else:
        if not isinstance(text, str):
            resp = dumps(text, indent=2)
        else:
            resp = text
    return resp


class MyFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(fmt=NEW_LOG_FORMAT, datefmt=NEW_DATE_FORMAT, style='{')

    def formatMessage(self, record: logging.LogRecord) -> str:
        text = _shorter_log_record(record.message)
        record.message = text
        return super().formatMessage(record)

    def formatException(self, exc_info: TracebackType) -> str:
        return _get_detailed_traceback(exc_info)


logger = logging.getLogger('bot')
handler = logging.StreamHandler()
handler.setFormatter(MyFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logger.propagate = False


def _sys_exc_handler(exc_type, exc_value, exc_tb):
    logging.error(_get_detailed_traceback((exc_type, exc_value, exc_tb)))


sys.excepthook = _sys_exc_handler
