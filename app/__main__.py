# -*- encoding: utf-8 -*-
"""Main module"""
import argparse
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from datetime import datetime
from telebox import Telebox
from .config import Config


def create_folder_if_not_exists(filename, folder_id):
    if not (pid := telebox.search.folder_exists(filename, folder_id)):
        # Folder not exists on telebox, create folder
        pid = telebox.folder.create(filename, folder_id)
    return pid


def upload_file_and_print_status(i, total, directory, file, subfolder_pid):
    print(f'{i + 1}/{total} - Uploading file: {file}')
    telebox.upload.upload_file(directory + '/' + file, subfolder_pid)


def main(arguments):
    logging.basicConfig(level=logging.ERROR)

    # Searching if the folder exists
    folder_pid = create_folder_if_not_exists(arguments.filename, Config.USR_BASEFOLDER)
    folder_data = telebox.search.search('', folder_pid)['data']['list']
    print('Get Main Folder PID for folder ' + arguments.filename + ' is ' + str(folder_pid))

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
            subfolder_pid = create_folder_if_not_exists(directory, folder_pid)
            if subfolder_pid == -1:
                sys.exit("Execution stopped. Folder not created")
        else:
            subfolder_pid = subfolder[0]['id']

        print('Creating or getting PID for folder:  ' + arguments.filename + '/' + directory + ' is ' + str(subfolder_pid))

        # Upload Files to Telebox
        print('Start Uploading....')
        file_list = os.listdir(arguments.dir + '/' + directory)
        len_list = str(len(file_list))
        with ThreadPoolExecutor(max_workers=3) as executor:
            for i, file in enumerate(file_list):
                executor.submit(upload_file_and_print_status, i, len_list, (arguments.dir + '/' + directory), file, subfolder_pid)

        # for file in file_list:
        #   i += 1
        #   print(str(i) + '/' + str(len(file_list)) + ' - Uploading file: ' + file)
        #   telebox.upload.upload_file(arguments.dir + '/' + directory + '/' + file, subfolder_pid)
        print('End Uploading....')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, help='Indica el nombre de la carpeta a buscar. Recuerda que debe existir también en la ruta en la que usarás con el parametro --dir.')
    parser.add_argument('--dir', type=str, help='Ruta donde se encuentra en tu equipo la carpeta con el nombre --filename')
    args = parser.parse_args()
    args.dir = args.dir.replace('\\', '\\\\') + '/' + args.filename
    telebox = Telebox(Config.USR_TOKEN, Config.USR_BASEFOLDER)
    datetime1 = datetime.now()
    print(f'Current date is: {datetime1.strftime("%Y-%m-%d %H:%M:%S")}')

    main(args)

    datetime2 = datetime.now()
    print(f'Current date is: {datetime2.strftime("%Y-%m-%d %H:%M:%S")}')
    # Get the difference between the datetimes
    diff = abs(datetime2 - datetime1)
    # Extract days, hours, minutes, and seconds
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)

    print(f"Total Time: {str(hours).zfill(2)}:{str(minutes).zfill(2)}:{str(seconds).zfill(2)}")
