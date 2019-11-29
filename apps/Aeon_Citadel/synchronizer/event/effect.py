class Effect:
    def __init__(self, effect, avatar):
        self.effect = effect
        self.avatar = avatar

    def execute_effect(self):
        res_type = self.effect.get('name', '')
        if res_type == 'heal':
            self.avatar.take_heal(self.effect.get('point', 0))
        elif res_type == 'damage':
            self.avatar.take_damage(self.effect.get('point', 0))

    def get_info(self):
        return self.effect.get('msg', "well... something happened...")
