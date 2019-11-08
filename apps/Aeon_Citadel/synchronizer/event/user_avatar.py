from .avatar import Avatar


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
            self.avatar['exp'] = exp - bound
            self.avatar['lv'] = int(self.avatar.get('lv', 1) + 1)
            self.check_level_up()
        else:
            self.avatar['exp'] = exp


def get_level_json(lv):
    json = {
        1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 7: 700
    }
    return json[lv]
