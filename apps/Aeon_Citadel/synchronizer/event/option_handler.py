from .effect import Effect
from .events import message_event
from .user_avatar import UserAvatar


class OptionHandler:
    def __init__(self, event, avatar):
        self.event = event
        self.options = event.get('results', {})
        self.avatar = avatar

    def handle_event(self, avatar_act):
        result = self.options.get(avatar_act, {})
        new_event = self.event
        user_avatar = UserAvatar(avatar_act, self.avatar)
        if result == {}:
            new_event['status'] = 'standby'
            new_event['next'] = message_event('无事发生')
        else:
            effect = Effect(result, user_avatar)
            effect.execute_effect()
            message = effect.get_info()
            new_event['status'] = 'end'
            new_event['next'] = message_event(message)
        new_avatar = user_avatar.get_avatar()
        return new_event, new_avatar

