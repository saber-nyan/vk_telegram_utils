import logging.config
import os
from typing import Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'logs')

log = logging.getLogger('vk-dumper.utils')


def str_none_or_empty(string: Optional[str]) -> bool:
    return not string or not string.strip()


def init_logging(debug: bool) -> None:
    log_all_file = os.path.join(LOG_DIR, 'vk_dumper.log')
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console_basic': {
                'format': '%(asctime)s [%(levelname)s] P%(process)d <%(filename)s:%(lineno)d'
                          ', %(funcName)s()> %(name)s: %(message)s',
            },
            'file_text': {
                'format': '%(asctime)s (+%(relativeCreated)d) [%(levelname)s] P%(process)d T%(thread)d'
                          ' <%(pathname)s:%(lineno)d, %(funcName)s at %(module)s> \'%(name)s\': %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'console_basic',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': log_all_file,
                'mode': 'wt',
                'encoding': 'utf-8',
                'formatter': 'file_text',
            },
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['console', 'file', ],
            },
            'vk-dumper': {
                'level': 'DEBUG',
                'handlers': ['console', 'file', ],
                'propagate': False,
            },
            'http.client': {
                'level': 'DEBUG',
                'handlers': ['console', 'file', ],
                'propagate': False,
            },
        },
    }
    logging.config.dictConfig(config)
    log.info('Initialised loggers, logging to file "%s"', log_all_file)
