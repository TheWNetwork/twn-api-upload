# -*- encoding: utf-8 -*-
"""Main module"""
import argparse

from datetime import datetime
from telebox_imp import TeleboxImpl
from terabox_imp import TeraboxImpl

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', type=str, help='Indica el nombre de la carpeta a buscar. Recuerda que debe existir también en la ruta en la que usarás con el parametro --dir.')
    parser.add_argument('--dir', type=str, help='Ruta donde se encuentra en tu equipo la carpeta con el nombre --filename')
    parser.add_argument('--telebox', type=int, help='Subir a Telebox')
    parser.add_argument('--terabox', type=int, help='Subir a Terabox')
    args = parser.parse_args()
    args.dir = args.dir.replace('\\', '\\\\') + '/' + args.filename
    datetime1 = datetime.now()
    print(f'Current date is: {datetime1.strftime("%Y-%m-%d %H:%M:%S")}')

    if (args.telebox):
        TeleboxImpl(args)

    # if(args.terabox):
    # Terabox(Config.TERABOX_API, Config.TERABOX_ROUTE)

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
