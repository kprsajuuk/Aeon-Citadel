from .synchronizer import sync_check
from .room.room_generator import generate_room
from .event.enemy_handler import EnemyHandler


def handle_action(event, action, avatar, difficulty):
    if not sync_check(event, action):
        return False
    if event is None or event == '':
        event = {'name': 'default'}

    if action == 'requestLatest':
        return event, avatar

    if action == 'newroom':
        event = generate_room(10)
    elif event['name'] == 'enemy':
        enemy_handler = EnemyHandler(event.get('enemy', {}), avatar)
        enemy, avatar = enemy_handler.handle_action(action)
        if enemy.get('dead', False) is True:
            del event['enemy']
            event['name'] = 'win'
        else:
            event['enemy'] = enemy
    return event, avatar
