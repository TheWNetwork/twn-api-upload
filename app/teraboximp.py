# -*- encoding: utf-8 -*-
"""Terabox Implementation module"""
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime
from terabox import Terabox
from .config import Config


class TeraboxImpl:
    terabox = None

    def __init__(self, arguments):
        self.terabox = Terabox(Config.TERABOX_API, Config.TERABOX_ROUTE)
        self.main(arguments)

    def upload_file_and_print_status(self, i, total, directory, file):
        print(f'{i + 1}/{total} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Uploading file: {file}')
        self.terabox.upload.invoke(directory + '/' + file)

    def main(self, arguments):
        print('Start Uploading....')
        file_list = os.listdir(arguments.dir)
        len_list = str(len(file_list))
        with ThreadPoolExecutor(max_workers=int(Config.USR_LIMIT_CONCURRENT)) as executor:
            for i, file in enumerate(file_list):
                executor.submit(self.upload_file_and_print_status, i, len_list, arguments.dir, file)

        # for file in file_list:
        #   i += 1
        #   print(str(i) + '/' + str(len(file_list)) + ' - Uploading file: ' + file)
        #   telebox.upload.upload_file(arguments.dir + '/' + directory + '/' + file, subfolder_pid)
        print('End Uploading....')
