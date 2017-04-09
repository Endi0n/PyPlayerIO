from playerio import *

client = Client('everybody-edits-su9rn58o40itdbnw69plyw', 'guest', 'guest')

players_online = 0

for room in client.list_rooms('Everybodyedits220'):
    print('{} - {} players online'.format(room.data['name'], room.online_users))
    players_online += room.online_users

print('Total: {} users\n'.format(players_online))

room = client.create_join_room('PWL17t1R6bbUI', 'Everybodyedits220', True)


@room.add_handler('playerio.connect')
def on_disconnect(message):
    print('Connected :)')


@room.add_handler('init')
def on_init(message):
    room.send('init2')


@room.add_handler('add')
def on_add(message):
    import time
    time.sleep(1)
    room.send('say', 'Hi {}!'.format(message[1].title()))


@room.add_handler('playerio.disconnect')
def on_disconnect(message):
    print('Disconnected :(')

room.send('init')
