class PlayerIOError(Exception):

    def __init__(self, error):
        self.__error = error

    def __str__(self):
        return f'Error code: {self.__error.code} - Message: {self.__error.message}'

    @property
    def code(self):
        return self.__error.code
    
    @property
    def message(self):
        return self.__error.message
