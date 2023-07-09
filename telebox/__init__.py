# telebox.py
import sys

import requests
from .config import Config


class Telebox:
    """
    The `Telebox` class represents a client to interact with the Telebox API.

    :param token: The access token required for authentication.
    :param folder_id: The ID of the folder to interact with.

    The class provides methods to connect, search, and perform various operations on the specified folder.

    Example usage:
        token = "your-access-token"
        folder_id = "your-folder-id"
        telebox = Telebox(token, folder_id)

    Methods:
        - connect: Connects to the Telebox server.
        - search: Searches for files in the specified folder.
        - folder: Retrieves information about the specified folder.

    Note:
        The class requires the Telebox library to be installed.

    """

    def __init__(self, token, folder_id):
        self.token = token
        self.folder_id = folder_id
        self.connect = Connect(Config.TELEBOX_BASE_URI, self.token)
        self.search = Search(self.connect)
        self.folder = Folder(self.connect)
        # self.upload_auth = UploadAuthorization(self.connect)
        # self.folder_details = FolderDetails(self.folder_id, self.connect)
        # self.folder_upload = FolderUploadFile(self.folder_id, self.connect)


class HttpClientService:
    """
    .. class:: HttpClientService

       The HttpClientService class provides methods to make HTTP GET and POST requests.

       :param base_url: The base URL that will be used for all requests.
       :type base_url: str

       .. method:: __init__(base_url)

          Constructs a new HttpClientService object.

          :param base_url: The base URL that will be used for all requests.
          :type base_url: str

       .. method:: get(endpoint, params=None)

          Sends an HTTP GET request to the specified endpoint.

          :param endpoint: The endpoint to send the request to.
          :type endpoint: str

          :param params: (optional) The query parameters to include in the request.
          :type params: dict

          :return: The JSON response from the server.
          :rtype: dict

          :raises requests.exceptions.HTTPError: If the request fails.

       .. method:: post(endpoint, params=None)

          Sends an HTTP POST request to the specified endpoint.

          :param endpoint: The endpoint to send the request to.
          :type endpoint: str

          :param params: (optional) The query parameters to include in the request.
          :type params: dict

          :return: The JSON response from the server.
          :rtype: dict

          :raises requests.exceptions.HTTPError: If the request fails.
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, params=None):
        response = requests.post(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()


class Connect:
    """
    Connect

    Class representing a connection to a remote server.

    Attributes:
        client (HttpClientService): The underlying HTTP client service.
        token (str): The authentication token.

    Methods:
        __init__(base_url, token)
            Initializes a new Connect instance.

        get_data(endpoint, params)
            Makes a GET request to the specified endpoint with the given parameters.

        post_data(endpoint, params)
            Makes a POST request to the specified endpoint with the given parameters.
    """

    def __init__(self, base_url, token):
        self.client = HttpClientService(base_url)
        self.token = token

    def get_data(self, endpoint, params):
        params["token"] = self.token
        return self.client.get(endpoint, params)

    def post_data(self, endpoint, params):
        params["token"] = self.token
        return self.client.post(endpoint, params)


class Search:
    """
     Initialize a Search object.

    Args:
        connect: The connection object used for making API calls.

    Attributes:
        connect: The connection object used for making API calls.
        url: The URL of the search file.
    """

    def __init__(self, connect):
        self.connect = connect
        self.url = Config.TELEBOX_SEARCH_FILE

    def search(self, filename, folder_id):
        return self.connect.get_data(self.url, {'pid': folder_id, 'name': filename, 'pageNo': 1, 'pageSize': 50})

    def folder_exists(self, filename, folder_id):
        lot = self.search(filename, folder_id)
        if isinstance(lot['data']['list'], list) and len(lot['data']['list']) != 0:
            return lot['data']['list'][0]['id'] if lot['data']['list'][0]['type'] == 'dir' and lot['data']['list'][0]['pid'] == int(folder_id) else False
        return False


class Upload:
    def __init__(self, user_id, connect):
        self.connect = connect

    def prepare(self):
        return self.connect.get_data(f"authorize?user_id={self.user_id}")


class Folder:
    """
     Class representing a folder.

    Args:
        connect: The connection object used to communicate with the server.

    Attributes:
        connect: The connection object used to communicate with the server.

    """

    def __init__(self, connect):
        self.connect = connect

    def create(self, filename, destination_folder_id):
        lot = self.connect.get_data(Config.TELEBOX_FOLDER_CREATE, {'pid': int(destination_folder_id), 'name': filename, 'isShare': 0, 'canInvite': 1, 'canShare': 1, 'withBodyImg': 0,
                                                                   'desc': 'TheWNetwork Telebox Mass Creator'})
        if lot['status'] != 1:
            sys.exit("Execution stopped. Cannot create folders")

        return lot['data']['dirId']

    def get_details(self, destination_folder_id):
        return self.connect.get_data(Config.TELEBOX_FOLDER_DETAILS, {'dirId': destination_folder_id})
