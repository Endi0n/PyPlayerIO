import urllib.request
import struct
from .error import PlayerIOError


class HTTPChannel:

    def __init__(self):
        self.token = None

    def request(self, method, input_message, output_message, error_message):
        # Initializing the request
        input_message = input_message.SerializeToString()
        headers = {}
        if self.token:
            headers['playertoken'] = self.token
        request = urllib.request.Request(f'http://api.playerio.com/api/{method}', input_message, headers)

        # Reading the response
        response = urllib.request.build_opener().open(request)

        # Getting the token if it exists
        has_token = ord(response.read(1))
        if has_token:
            length = struct.unpack(">H", response.read(2))[0]
            self.token = (response.read(length)).decode('utf8')

        # Checking the status
        status = ord(response.read(1))
        if status:
            if status == 1:
                output_message.ParseFromString(response.read())
        else:
            error_message.ParseFromString(response.read())
            raise PlayerIOError(error_message)
