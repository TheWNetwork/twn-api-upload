# -*- encoding: utf-8 -*-
"""Config vars module"""
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


class Config(object):
    USR_LIMIT_CONCURRENT = os.environ.get('USR_LIMIT_CONCURRENT')
    TELEBOX_API = os.environ.get('TELEBOX_API')
    TELEBOX_BASEFOLDER = os.environ.get('TELEBOX_BASEFOLDER')
    TERABOX_API = os.environ.get('TERABOX_API')
    TERABOX_ROUTE = os.environ.get('TERABOX_ROUTE')
