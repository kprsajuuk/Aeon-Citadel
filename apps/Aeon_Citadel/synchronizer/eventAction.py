from .synchronizer import sync_check
from .room.map_calculator import next_room
from .room.room_generator import generate_map, generate_room
from .event.enemy_handler import EnemyHandler
from .event.option_handler import OptionHandler
from .event.message_handler import MessageHandler
from django.forms.models import model_to_dict
from Aeon_Citadel.models import Journey


def update_journey(avatar_id, avatar_act):
    event, event_que, avatar, map_user, map_level, difficulty = get_journey(avatar_id)
    if not avatar:
        return False, False
    success, data = handle_action(event, event_que, avatar_act, avatar, avatar_id, map_user,
                                  map_level, difficulty)
    return success, data


def handle_action(event, event_que, action, avatar, avatar_id, map_user, map_level, dif):
    if not sync_check(event, action):
        return False, False

    if event == '':
        if not event_que:
            event = {'type': 'start', 'content': {'name': 'start'}}
        else:
            event = event_que.pop(0)
        Journey.objects.filter(avatar_id=avatar_id).update(event_current=event, event_queue=event_que)

    result = {"event": event.get('content', {}), "hero": avatar}
    if action == 'requestLatest':
        result['map'] = map_user
        return True, result

    if event['type'] == 'start':
        room_number, map_level = generate_map(10)
        room_user = map_level[room_number]
        room_user['user'] = True
        room_user['show'] = True
        map_user = {'user': room_number}
        rooms = []
        for room in map_level:
            rooms.append(room if room == room_user else {"coor": room.get('coor', []), "show": False})
        map_user['rooms'] = rooms
        Journey.objects.filter(avatar_id=avatar_id).update(map_level=map_level, map_user=map_user)

        event = {'type': 'move', 'content': {'name': 'move', 'path': room_user.get('path', [])}}
        result['map'] = map_user
    elif event['type'] == 'move':
        new_room, new_map_user = next_room(action, map_user, map_level)
        Journey.objects.filter(avatar_id=avatar_id).update(map_user=new_map_user)
        result['map'] = new_map_user
        user_num = new_map_user['user']
        new_room_user = new_map_user['rooms'][user_num]
        event_que = generate_room(new_room, new_room_user)
        event = event_que.pop(0)

    elif event['type'] == 'enemy':
        enemy_handler = EnemyHandler(event, avatar)
        event, avatar = enemy_handler.handle_action(action)
    elif event['type'] == 'message':
        message_handler = MessageHandler(event, avatar)
        event, avatar = message_handler.handle_action(action)
    elif event['type'] == 'option':
        option_handler = OptionHandler(event, avatar)
        event, avatar = option_handler.handle_event(action)

    event, event_que = after_event(avatar_id, event, event_que)
    Journey.objects.filter(avatar_id=avatar_id).update(event_current=event, avatar_status=avatar,
                                                       event_queue=event_que)
    result['event'] = event.get('content', {})
    result['hero'] = avatar
    return True, result


def get_journey(avatar_id):
    journey = model_to_dict(Journey.objects.filter(avatar_id=avatar_id)[0])
    # noinspection PyBroadException
    try:
        event = eval(journey['event_current'])
        event_que = eval(journey['event_queue'])
        map_user = eval(journey['map_user'])
        map_level = eval(journey['map_level'])
    except Exception:
        event = ''
        event_que = []
        map_user = []
        map_level = []
    # noinspection PyBroadException
    try:
        avatar = eval(journey['avatar_status'])
        difficulty = int(journey['difficulty'])
    except Exception:
        avatar = False
        difficulty = False
    return event, event_que, avatar, map_user, map_level, difficulty


def get_journey_detail(avatar_id, fields):
    journey = model_to_dict(Journey.objects.filter(avatar_id=avatar_id)[0])
    data_list = []
    for field in fields:
        # noinspection PyBroadException
        try:
            data = eval(journey[field])
        except Exception:
            data = False
        data_list.append(data)
    return data_list


def after_event(avatar_id, event, event_que):
    if event.get('status', '') == 'end':
        if event.get('next', {}) != {}:
            event = event['next']
        elif len(event_que) > 0:
            event = event_que.pop(0)
        else:
            map_level = get_journey_detail(avatar_id, ['map_user'])[0]
            room_user = map_level['rooms'][map_level['user']]
            event = {'type': 'move', 'content': {'name': 'move', 'path': room_user.get('path', [])}}

    return event, event_que
# 可能需要before event方法
