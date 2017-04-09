class PlayerIOError(Exception):

    def __init__(self, error):
        self.__error = error

    def __str__(self):
        return 'Code {}, {}'.format(self.__error.code, self.__error.message)
