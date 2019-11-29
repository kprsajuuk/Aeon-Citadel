from .effect import Effect
from .events import message_event
from .user_avatar import UserAvatar


class MessageHandler:
    def __init__(self, event, avatar):
        self.event = event
        self.avatar = avatar

    def handle_action(self, action):
        result = self.event.get('result', {})
        user_avatar = UserAvatar(action, self.avatar)
        new_event = self.event
        if result == {}:
            new_event['status'] = 'end'
        else:
            effect = Effect(result, user_avatar)
            effect.execute_effect()
            message = effect.get_info()
            new_event = message_event(message)
        new_avatar = user_avatar.get_avatar()
        return new_event, new_avatar
