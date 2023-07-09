# -*- encoding: utf-8 -*-
"""Config vars module"""
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

class Config(object):
    USR_TOKEN = os.environ.get('USR_TOKEN')
    USR_BASEFOLDER = os.environ.get('USR_BASEFOLDER')
