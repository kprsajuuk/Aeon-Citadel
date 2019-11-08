import random
from .avatar import Avatar
from .user_avatar import UserAvatar


class EnemyHandler:
    def __init__(self, enemy, avatar):
        self.enemy = enemy
        self.avatar = avatar
        self.action = random.sample(['attack', 'dodge', 'charge'], 1)[0]

    def handle_action(self, avatar_act):
        user_avatar = UserAvatar(avatar_act, self.avatar)
        enemy_avatar = Avatar(self.action, self.enemy)

        user_avatar.before_action()
        enemy_avatar.before_action()
        user_avatar.execute_action(enemy_avatar)
        enemy_avatar.execute_action(user_avatar)
        user_avatar.after_action()
        enemy_avatar.after_action()

        enemy = enemy_avatar.get_avatar()
        if enemy.get('dead', False) is True:
            self.handle_defeat_enemy(user_avatar)
        avatar = user_avatar.get_avatar()

        return enemy, avatar

    def handle_defeat_enemy(self, user_avatar):
        exp = self.enemy.get('lv', 0) * 10
        user_avatar.get_exp(exp)

