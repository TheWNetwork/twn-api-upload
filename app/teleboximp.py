# -*- encoding: utf-8 -*-
"""Terabox Implementation module"""
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime
from telebox import Telebox
from .config import Config


class TeleboxImpl:
    telebox = None

    def __init__(self, arguments):
        self.telebox = Telebox(Config.TELEBOX_API, Config.TELEBOX_BASEFOLDER)
        self.main(arguments)

    def create_folder_if_not_exists(self, foldername, folder_id):
        if not (pid := self.telebox.search.folder_exists(foldername, folder_id)):
            # Folder not exists on telebox, create folder
            pid = self.telebox.folder.create(foldername, folder_id)
        return pid

    def upload_file_and_print_status(self, i, total, directory, file, subfolder_pid):
        print(f'{i + 1}/{total} - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - Uploading file: {file}')
        self.telebox.upload.upload_file(directory + '/' + file, subfolder_pid)

    def doit(self, file_list, len_list, directory, folder_pid):
        with ThreadPoolExecutor(max_workers=int(Config.USR_LIMIT_CONCURRENT)) as executor:
            for i, file in enumerate(file_list):
                if os.path.isfile(directory + '/' + file):
                    executor.submit(TeleboxImpl.upload_file_and_print_status, self, i, len_list, directory, file, folder_pid)

    def main(self, arguments):
        logging.basicConfig(level=logging.ERROR)

        # Searching if the folder exists
        folder_pid = self.create_folder_if_not_exists(arguments.foldername, Config.TELEBOX_BASEFOLDER)
        folder_data = self.telebox.search.search('', folder_pid)['data']['list']
        print('Get Main Folder PID for folder ' + arguments.foldername + ' is ' + str(folder_pid))
        self.doit(os.listdir(arguments.dir), str(len(os.listdir(arguments.dir))), arguments.dir, folder_pid)

        directories = [d for d in os.listdir(arguments.dir) if os.path.isdir(os.path.join(arguments.dir, d))]
        for directory in directories:
            # Create or get Folder IDs

            print('\n\n######################################')

            if folder_data:
                subfolder = list(filter(lambda d: d['name'] == directory, folder_data))
            else:
                subfolder = None

            if not subfolder:
                # Not created yet
                subfolder_pid = self.create_folder_if_not_exists(directory, folder_pid)
                if subfolder_pid == -1:
                    sys.exit("Execution stopped. Folder not created")
            else:
                subfolder_pid = subfolder[0]['id']

            print('Creating or getting PID for folder:  ' + arguments.foldername + '/' + directory + ' is ' + str(subfolder_pid))

            # Upload Files to Telebox
            print('Start Uploading....')
            file_list = os.listdir(arguments.dir + '/' + directory)
            len_list = str(len(file_list))
            self.doit(file_list, len_list, arguments.dir + '/' + directory, subfolder_pid)

            # for file in file_list:
            #   i += 1
            #   print(str(i) + '/' + str(len(file_list)) + ' - Uploading file: ' + file)
            #   telebox.upload.upload_file(arguments.dir + '/' + directory + '/' + file, subfolder_pid)
            print('End Uploading....')


