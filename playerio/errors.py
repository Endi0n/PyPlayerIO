class PlayerIOError(Exception):

    def __init__(self, value):
        self.value = value.message

    def __str__(self):
        return repr(self.value)
