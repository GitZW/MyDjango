"""
Django settings for server_api project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
CONF_FILE = "/.gf_conf_test"

import os
from .base import *

from utils.common import gf_conf

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'gf_app_test',
        'USER': 'root',
        'PASSWORD': gf_conf.get_value('app_mysql_pwd'),
        'OPTIONS': {'charset': 'utf8mb4'},
        'CONN_MAX_AGE': 20000
    }
}

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.handlers.WatchedFileHandler',
            # 'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
            'filename': gf_conf.get_value("app_console_log_file"),

        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
    'loggers': {
        'django.db.backends': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': False,
        }
    }
}
