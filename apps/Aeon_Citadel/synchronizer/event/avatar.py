class Avatar:
    def __init__(self, action, avatar):
        self.action = action
        self.avatar = avatar

    def before_action(self):
        print(self.action)
        if self.action == 'attack':
            self.before_attack()
        elif self.action == 'dodge':
            self.before_dodge()
        elif self.action == 'charge':
            self.before_charge()

    def execute_action(self, enemy):
        print(self.action)
        if self.action == 'attack':
            self.execute_attack(enemy)
        elif self.action == 'dodge':
            self.execute_dodge()
        elif self.action == 'charge':
            self.execute_charge()

    def after_action(self):
        if self.action == 'attack':
            self.after_attack()
        elif self.action == 'dodge':
            self.after_dodge()
        elif self.action == 'charge':
            self.after_charge()

    def get_avatar(self):
        return self.avatar

    def cal_damage(self):
        atk = int(self.avatar.get('attack', 0))
        crg = int(self.avatar.get('charge', 0))
        return (atk + crg) * (crg + 1)

    def before_attack(self):
        self.avatar['description'] = self.avatar['name'] + "使用了攻击"

    def execute_attack(self, enemy):
        dmg = self.cal_damage()
        enemy.take_attack(dmg)

    def after_attack(self):
        self.avatar['charge'] = 0
        self.avatar['stamina'] = min(int(self.avatar.get('stamina', 0)) + 1, int(self.avatar.get('max_stamina', 2)))

    def before_dodge(self):
        sta = int(self.avatar.get('stamina', 0))
        self.avatar['description'] = self.avatar['name'] + "使用了闪避"
        if not sta > 0:
            self.action = 'default'
            self.avatar['description'] += "但是失败了"

    def execute_dodge(self):
        pass

    def after_dodge(self):
        self.avatar['stamina'] = max(int(self.avatar.get('stamina', 0)) - 1, 0)

    def before_charge(self):
        self.avatar['charge'] = int(self.avatar.get('charge', 0)) + 1
        self.avatar['description'] = self.avatar['name'] + "使用了蓄力"

    def execute_charge(self):
        pass

    def after_charge(self):
        self.avatar['stamina'] = min(int(self.avatar.get('stamina', 0)) + 1, 2)

    def take_attack(self, dmg):
        if self.action != 'dodge':
            dmg = max(dmg - self.cal_damage(), 0) if self.action == 'attack' else dmg
            self.take_damage(dmg)

        if int(self.avatar['hp']) <= 0:
            self.avatar['hp'] = 0
            self.avatar['dead'] = True

    def take_damage(self, dmg):
        self.avatar['hp'] = int(self.avatar['hp']) - int(dmg)

    def take_heal(self, hp):
        self.avatar['hp'] = min(int(self.avatar['hp']) + int(hp), int(self.avatar.get('max_hp', 0)))
