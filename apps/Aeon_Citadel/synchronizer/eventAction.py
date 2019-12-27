from .synchronizer import sync_check
from .room.map_calculator import next_room
from .room.room_generator import generate_map, leave_room, enter_room
from .event.enemy_handler import EnemyHandler
from .event.option_handler import OptionHandler
from .event.message_handler import MessageHandler
from .event.events import message_event
from django.forms.models import model_to_dict
from Aeon_Citadel.models import Journey


class ActionHandler:
    def __init__(self, avatar_id, avatar_action):
        self.avatar_id = avatar_id
        self.avatar_action = avatar_action
        self.journey = {}
        self.new_journey = {}

    def handle_journey(self):
        self.get_journey()
        data = self.get_journey_detail(['avatar_status', 'difficulty'])
        avatar = data.get('avatar_status', {})
        difficulty = data.get('difficulty', 10)
        avatar['description'] = ""
        success, data = self.handle_action(avatar, difficulty)
        self.update_journey()
        return success, data

    def get_journey(self):
        journey = model_to_dict(Journey.objects.filter(avatar_id=self.avatar_id)[0])
        self.journey = journey

    def get_journey_detail(self, fields):
        data_obj = {}
        for field in fields:
            # noinspection PyBroadException
            try:
                data = eval(self.journey[field])
            except Exception:
                data = self.journey[field]
            data_obj[field] = data
        return data_obj

    def handle_action(self, avatar, dif):
        data = self.get_journey_detail(['event_current', 'event_queue'])
        event = data.get('event_current', {})
        event_que = data.get('event_queue', [])

        if not sync_check(event, self.avatar_action):
            return False, False

        if event == {}:
            if not event_que:
                event = {'type': 'start', 'content': {'name': 'start'}}
            else:
                event = event_que.pop(0)
        self.new_journey = {'event_current': event, 'event_queue': event_que}
        result = {"event": event.get('content', {}), "hero": avatar}
        if self.avatar_action == 'requestLatest':
            result['map'] = self.get_journey_detail(['map_user'])['map_user']
            return True, result

        if event['type'] == 'start':
            room_number, map_level = generate_map(dif)
            room_user = map_level[room_number]
            room_user['user'] = True
            room_user['show'] = True
            map_user = {'user': room_number}
            rooms = []
            for room in map_level:
                rooms.append(room if room == room_user else {"coor": room.get('coor', []), "show": False})
            map_user['rooms'] = rooms
            self.new_journey['map_level'] = map_level
            self.new_journey['map_user'] = map_user
            event = {'type': 'move', 'content': {'name': 'move', 'path': room_user.get('path', [])}}
            result['map'] = map_user
        elif event['type'] == 'journey_end':
            return True, result
        elif event['type'] == 'move':
            data = self.get_journey_detail(['map_level', 'map_user'])
            map_level = data['map_level']
            map_user = data['map_user']
            if self.avatar_action == 'act':
                if len(event_que) > 0:
                    event = event_que.pop(0)
                    if event['status'] == 'standby':
                        event['status'] = 'start'
                    map_level[map_user['user']]['events'] = event_que
                    if len(event_que) <= 0:
                        map_user['rooms'][map_user['user']]['act'] = False
                    self.new_journey['map_level'] = map_level
                    self.new_journey['map_user'] = map_user
                else:
                    event = message_event('什么都没有发现qaq')
            else:
                leave_room(self.avatar_action, map_level, map_user)
                new_map_user = next_room(self.avatar_action, map_level, map_user)
                if not new_map_user:
                    return False, False
                result['map'] = new_map_user
                room_num = new_map_user['user']

                event_que = enter_room(room_num, map_level, new_map_user)
                event = event_que.pop(0)
                self.new_journey['map_level'] = map_level
                self.new_journey['map_user'] = new_map_user

        elif event['type'] == 'enemy':
            enemy_handler = EnemyHandler(event, avatar)
            event, avatar = enemy_handler.handle_action(self.avatar_action)
        elif event['type'] == 'message':
            message_handler = MessageHandler(event, avatar)
            event, avatar = message_handler.handle_action(self.avatar_action)
        elif event['type'] == 'option':
            option_handler = OptionHandler(event, avatar)
            event, avatar = option_handler.handle_event(self.avatar_action)

        event, event_que = self.after_event(event, event_que)
        self.new_journey['event_current'] = event
        self.new_journey['event_queue'] = event_que
        self.new_journey['avatar_status'] = avatar

        if avatar.get('hp', 0) <= 0:
            avatar['status'] = 'death'
            event['status'] = 'end'
            event['type'] = 'pass'
            event['next'] = {
                "type": "journey_end",
                "journey": "lost",
                "content": {"name": "journey_end", "journey": "lost"},
            }
        result['event'] = event.get('content', {})
        result['hero'] = avatar
        return True, result

    def after_event(self, event, event_que):
        status = event.get('status', {})
        if status != 'end' and status != 'standby':
            return event, event_que

        if status == 'standby':
            event_que.append(event)
        if event.get('next', {}) != {}:
            new_event = event['next']
            del event['next']
        elif len(event_que) > 0 and event_que[0].get('status', {}) != 'standby':
            new_event = event_que.pop(0)
        else:
            map_level = self.new_journey.get('map_level', self.get_journey_detail(['map_level'])['map_level'])
            map_user = self.new_journey.get('map_user', self.get_journey_detail(['map_user'])['map_user'])
            room_user = map_user['rooms'][map_user['user']]
            new_event = {'type': 'move', 'content': {'name': 'move', 'path': room_user.get('path', [])}}
            if len(event_que) > 0:
                map_level[map_user['user']]['events'] = event_que
                room_user['act'] = True
                new_event['content']['act'] = True
                self.new_journey['map_level'] = map_level
                self.new_journey['map_user'] = map_user

        return new_event, event_que
    # 可能需要before event方法

    def update_journey(self):
        Journey.objects.filter(avatar_id=self.avatar_id).update(**self.new_journey)
