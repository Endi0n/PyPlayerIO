class EventHandler:

    __handlers = {}

    def __init__(self):
        raise NotImplementedError("EventHandler is a static class!")

    @staticmethod
    def add(message_type='playerio.message'):
        def event_handler(func):
            if message_type not in EventHandler.__handlers:
                EventHandler.__handlers[message_type] = []
                EventHandler.__handlers[message_type].append(func)
        return event_handler

    @staticmethod
    def broadcast(room, message):
        if 'playerio.message' in EventHandler.__handlers:
            for handler in EventHandler.__handlers['playerio.message']:
                handler(room, message)
        if message.type in EventHandler.__handlers:
            for handler in EventHandler.__handlers[message.type]:
                handler(room, message)
