from .effect import Effect
from .events import message_event
from .user_avatar import UserAvatar


class OptionHandler:
    def __init__(self, event, avatar):
        self.event = event
        self.options = event.get('result', {})
        self.avatar = avatar

    def handle_event(self, avatar_act):
        result = self.options.get(avatar_act, {})
        user_avatar = UserAvatar(avatar_act, self.avatar)
        if result == {}:
            new_event = message_event('nothing happended')
        else:
            effect = Effect(result, user_avatar)
            effect.execute_effect()
            message = effect.get_info()
            new_event = message_event(message)
        new_avatar = user_avatar.get_avatar()
        return new_event, new_avatar

