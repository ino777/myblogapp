""" Settings of logging"""
import logging

# logging configuration
_config = {
    'version': 1,
    'formatters':{
        'blogsFormatter':{
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        }
    },
    'handlers':{
        'consoleHandler':{
            'class': 'logging.StreamHandler',
            'formatter': 'blogsFormatter',
            'level': logging.DEBUG,
        },
        'fileHandler':{
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'blogsFormatter',
            'filename': 'logging.log',
            'backupCount': 3,
            'encoding': 'utf-8',
            'level': logging.WARNING,
        },
    },
    'root':{
        'handlers': ['consoleHandler', 'fileHandler'],
        'level': logging.WARNING,
    },
    'loggers':{
        'blogsLogger':{
            'handlers': ['consoleHandler', 'fileHandler'],
            'level': logging.DEBUG,
            'propagate': False
        }
    }
}



#  password filter
class NoPassFilter(logging.Filter):
    def filter(self, record):
        log_message = record.getMessage()
        return 'password' not in log_message