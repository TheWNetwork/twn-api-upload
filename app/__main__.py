# -*- encoding: utf-8 -*-
"""Main module"""
import argparse
import logging
import os
import sys

from telebox import Telebox
from .config import Config


def create_folder_if_not_exists(filename, folder_id):
    if not (pid := telebox.search.folder_exists(filename, folder_id)):
        # Folder not exists on telebox, create folder
        pid = telebox.folder.create(filename, folder_id)
    return pid

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

        subfolder = list(filter(lambda d: d['name'] == directory, folder_data))
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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', type=str, help='Indica el nombre de la carpeta a buscar. Recuerda que debe existir también en la ruta en la que usarás con el parametro --dir.')
    parser.add_argument('--dir', type=str, help='Ruta donde se encuentra en tu equipo la carpeta con el nombre --filename')
    args = parser.parse_args()
    args.dir = args.dir.replace('\\', '\\\\') + '/' + args.filename
    telebox = Telebox(Config.USR_TOKEN, Config.USR_BASEFOLDER)
    main(args)
