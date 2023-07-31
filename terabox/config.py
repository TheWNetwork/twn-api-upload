# -*- encoding: utf-8 -*-
"""Config vars module"""


class Config(object):
    TERABOX_BASE = 'https://www.terabox.com/rest/2.0/xpan/file'
    TERABOX_UPLOAD = 'https://c-jp.terabox.com/rest/2.0/pcs/superfile2'
    TERABOX_CHUNK_SIZE = 1024 * 1024 * 4 # 4MB
