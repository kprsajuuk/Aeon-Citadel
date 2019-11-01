from .synchronizer import sync_check
from .room.room_generator import generate_room


def handle_action(event, action):
    if not sync_check(event, action):
        return False
    if event is None or action == 'newroom':
        event = generate_room(10)
    elif action == 'attack':
        handle_attack(event)
    return event


def handle_attack(event):
    event['enemy']['hp'] -= 10
