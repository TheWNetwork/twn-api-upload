# telebox.py
import sys

import os
from pathlib import Path

import json
import requests

import hashlib
from .config import Config
from urllib.parse import urlencode


class Terabox:

    def __init__(self, token, folder_location):
        self.token = token
        self.folder_location = folder_location
        self.connect = HttpClientService(Config.TERABOX_BASE, self.token)
        self.upload = Upload(self.connect, folder_location, Config.TERABOX_CHUNK_SIZE, )


class HttpClientService:

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def post_direct(self, endpoint, get_params=None, post_params=None, headers=None):
        get_params["access_tokenx"] = self.token
        response = requests.post(f"{self.add_params_to_url(endpoint, get_params)}", data=post_params, headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, get_params=None, post_params=None):
        return self.post_direct(f"{self.base_url}/{endpoint}", get_params, post_params)

    @staticmethod
    def add_params_to_url(url, get_params=None):
        if get_params:
            url += '?' + urlencode(get_params)
        return url


class Upload:
    def __init__(self, connect, file_location, chunk_size):
        self.connect = connect
        self.file_location = file_location
        self.chunk_size = chunk_size

    def invoke(self, filename):
        prepare_response = self.prepare(filename)
        if prepare_response.status_code != 200:
            print(f"Error occurred while preparing file: {filename}")
            return False

        upload_response = self.upload(filename, prepare_response)
        if not upload_response:
            print(f"Error occurred while uploading file: {filename}")
            return False

        complete_response = self.complete(filename, prepare_response)
        if complete_response.status_code != 200:
            print(f"Error occurred while completing file: {filename}")
            return False

        return True

    def prepare(self, filename):
        self.size = os.path.getsize(filename)
        self.chunk_hashes = []
        with open(filename, "rb") as f:
            while chunk := f.read(self.chunk_size):
                chunk_md5 = hashlib.md5(chunk).hexdigest()
                self.chunk_hashes.append(chunk_md5)

        # Call the Request method with all the MD5 blocks
        response = self.connect.post('', {'method': 'precreate', 'path': self.file_location, 'autoinit': 1, 'size': self.size, 'block_list': self.chunk_hashes})
        return response

    def upload(self, filename, prepare_response):
        file_size = os.path.getsize(filename)

        # Open file in binary mode
        with (open(filename, 'rb') as file):
            chunk_no = 0
            while True:
                # read only specified bytes amount (chunk_size)
                chunk = file.read(self.chunk_size)
                if not chunk:
                    break

                # Here you can make a request with the chunk
                # update 'YOUR_API_URL' with your actual API which will receive chunk data
                get = {
                    'method': 'upload',
                    'path': self.file_location,
                    'uploadid': 'UPLOAD_ID',
                    'partseq': chunk_no
                }

                headers = {
                    'Content-Range': f'bytes {chunk_no * self.chunk_size}-{(chunk_no + 1) * self.chunk_size - 1}/{file_size}',
                    # specify additional headers as per requirement of your API
                }

                response = self.connect.post_direct(Config.TERABOX_UPLOAD, get_params=get, post_params={file: chunk}, headers=headers)

                if response.status_code != 200:
                    print(f"Error occurred while uploading chunk: {chunk_no}")
                    return False

                chunk_no += 1

        return True

    def complete(self, filename, prepare_response):
        response = self.connect.post('',
                                     get_params={'method': 'create'},
                                     post_params={'path': self.file_location, 'size': self.size, 'uploadid': 'UPLOAD_ID', 'block_list': self.chunk_hashes})
        return response
