from playerio import *

if __name__ == "__main__":
    client = Client('everybody-edits-su9rn58o40itdbnw69plyw', 'ywambolt@hotmail.com', 'barbie')

    config = client.BigDB.load("config", ["config"])[0]
    version = next(p.value.int32 for p in config.properties if p.name == 'version')

    players_online = 0

    for room in client.list_rooms(f'Everybodyedits{version}'):
        print('{} - {} players online'.format(room.data['name'], room.online_users))
        players_online += room.online_users
    print('Total: {} users\n'.format(players_online))

    room = client.create_join_room('PWKpWR8Pb7cEI', f'Everybodyedits{version}', True)
    room.send('init')

@EventHandler.add()
def on_message(room, message):
    print(message)

@EventHandler.add('init')
def on_init(room, message):
    room.send('init2')

@EventHandler.add("say")
def on_say(room, message):
    print(message)


@EventHandler.add('add')
def on_add(room, message):
    import time
    time.sleep(1)
    room.send('say', 'Hi {}!'.format(message[1].title()))


@EventHandler.add('playerio.disconnect')
def on_disconnect(room, message):
    print('Disconnected :(')
