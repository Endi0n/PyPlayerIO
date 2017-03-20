from playerio.sdk import *

client = Client('everybody-edits-su9rn58o40itdbnw69plyw', '<snip>', '<snip>')

players_online = 0

for room in client.list_rooms('Everybodyedits220'):
    print('{} - {} players online'.format(room.data['name'], room.online_users))
    players_online += room.online_users

print('Total: {} users\n'.format(players_online))

room = client.create_join_room('<snip>', 'Everybodyedits220', True)


@room.add_event_handler('init')
def on_init(message):
    room.send('init2')


@room.add_event_handler('add')
def on_add(message):
    import time
    time.sleep(1)
    room.send('say', 'Hi {}!'.format(message[1].title()))


room.send('init')
