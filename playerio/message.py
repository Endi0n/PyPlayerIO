class Message:

    def __init__(self, message_type, *args):
        self.__type = message_type
        self.__args = list(args)

    def __len__(self):
        return len(self.__args)

    def __getitem__(self, item):
        return self.__args[item]

    def __str__(self):
        return '{} - {}'.format(self.__type, self.__args)

    @property
    def type(self):
        return self.__type

    @property
    def args(self):
        return self.__args

    def extend(self, *args):
        self.__args.extend(list(args))
