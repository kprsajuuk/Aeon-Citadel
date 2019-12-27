from .avatar import Avatar
from Aeon_Global import avatar_config


class UserAvatar(Avatar):
    def __init__(self, action, avatar):
        Avatar.__init__(self, action, avatar)

    def get_exp(self, exp):
        self.avatar['exp'] = int(self.avatar.get('exp', 0)) + exp
        self.check_level_up()

    def check_level_up(self):
        exp = int(self.avatar.get('exp', 0))
        bound = get_level_json(self.avatar['lv'])
        if exp >= bound:
            self.level_up()
            self.avatar['exp'] = exp - bound
            self.check_level_up()
        else:
            self.avatar['exp'] = exp

    def level_up(self):
        self.avatar['lv'] = int(self.avatar.get('lv', 1) + 1)
        self.avatar['skill_points'] = self.avatar.get('skill_points', 0) + 1


def get_level_json(lv):
    return avatar_config.level_bound.get(lv, 9999999)
