# PyPlayerIO
![alt tag](https://puu.sh/uRYjD/e2c412ce60.png)

A Python PlayerIOClient Implementation


## Getting Started

Download this repository and install protobuf with pip:

```
pip3 install "protobuf>=3.4.0,<3.7"
```


## Simple Application

```python
# Import the library
from playerio import *


# Connect to the game
client = Client('everybody-edits-su9rn58o40itdbnw69plyw', 'guest', 'guest')

# Get the game version from BigDB
version = client.bigdb_load('config', 'config')['version']

# Count the number of players online
players_online = 0

for room in client.list_rooms(f'Everybodyedits{version}'):
    print(f"{room.data['name']} - {room.players_online} players online")
    players_online += room.players_online

print(f'Total: {players_online} users\n')


# Join a room
room = client.create_join_room('PWL17t1R6bbUI', f'Everybodyedits{version}', True)

# Send a message
room.send('init')

# Print all the incoming events from the room
@EventHandler.add()
def on_message(room, message):
    print(message)

# Handle the init event
@EventHandler.add('init')
def on_init(room, message):
    room.send('init2')

# Handle a join event
@EventHandler.add('add')
def on_add(room, message):
    import time
    time.sleep(1)
    room.send('say', f'Hi {message[1].title()}!')

# Handle disconnection
@EventHandler.add('playerio.disconnect')
def on_disconnect(room, message):
    print('Disconnected :(')
```


## License

Based on [OpenPlayerIO Client](https://github.com/OpenPlayerIO/PlayerIOClient)

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-sa/4.0/

![alt tag](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)
