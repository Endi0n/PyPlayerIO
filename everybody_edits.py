from playerio import *

client = Client('everybody-edits-su9rn58o40itdbnw69plyw', 'guest', 'guest')

players_online = 0

for room in client.list_rooms('Everybodyedits228'):
    print('{} - {} players online'.format(room.data['name'], room.players_online))
    players_online += room.players_online

print('Total: {} players\n'.format(players_online))

room = client.create_join_room('PWL17t1R6bbUI', 'Everybodyedits220', True)
print('Connected :)')
room.send('init')


@EventHandler.add()
def on_message(room, message):
    print(message)


@EventHandler.add('init')
def on_init(room, message):
    room.send('init2')


@EventHandler.add('add')
def on_add(room, message):
    import time
    time.sleep(1)
    room.send('say', 'Hi {}!'.format(message[1].title()))


@EventHandler.add('playerio.disconnect')
def on_disconnect(room, message):
    print('Disconnected :(')