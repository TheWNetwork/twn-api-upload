# -*- encoding: utf-8 -*-
"""Main module"""
import argparse

from datetime import datetime

from app.teleboximp import TeleboxImpl
from app.teraboximp import TeraboxImpl

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--telebox', type=bool, help='Subir a Telebox', nargs='*')
    parser.add_argument('--terabox', type=bool, help='Subir a Terabox', nargs='*')
    parser.add_argument('--dir', type=str, help='Ruta donde se encuentra en tu equipo la carpeta con el nombre --foldername')
    parser.add_argument('--foldername', type=str, help='Indica el nombre de la carpeta a buscar. Recuerda que debe existir también en la ruta en la que usarás con el parametro --dir.')
    args = parser.parse_args()
    args.dir = args.dir.replace('\\', '\\\\') + '/' + args.foldername
    datetime1 = datetime.now()
    print(f'Current date is: {datetime1.strftime("%Y-%m-%d %H:%M:%S")}')

    if args.telebox != None:
        print('Telebox')
        TeleboxImpl(args)

    if args.terabox != None:
        print('Terabox')
        TeraboxImpl(args)

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
