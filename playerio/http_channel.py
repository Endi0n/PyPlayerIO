import urllib.request
import struct
from .errors import PlayerIOError


class HTTPChannel:

    def __init__(self):
        self.token = None

    def request(self, method, message_in, message_out, message_error):
        # Initializing request
        message_in = message_in.SerializeToString()
        headers = {}
        if self.token:
            headers['playertoken'] = self.token
        req = urllib.request.Request('http://api.playerio.com/api/{}'.format(method), message_in, headers)

        # Reading the response
        res = urllib.request.build_opener().open(req)

        # Getting the token if exists
        has_token = ord(res.read(1))
        if has_token:
            length = struct.unpack(">H", res.read(2))[0]
            self.token = (res.read(length)).decode('utf8')

        # Checking the status
        status = ord(res.read(1))
        if status:
            if status == 1:
                message_out.ParseFromString(res.read())
        else:
            message_error.ParseFromString(res.read())
            raise PlayerIOError(message_error)
