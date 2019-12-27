import random


def generate_map(dif):
    enemy = generate_enemy(dif)
    boss = generate_boss(dif)
    level_map = [
            {"type": 0,"coor": [1,1]},{"type": 0, "coor": [1,2]},{"type": 1, "coor": [1,3], "path": ['r', 'b']},{"type": 0,"coor": [1,4], "path": ['l','r']},{"type": 0,"coor": [1,5], "path": ['l'], "events": [boss]},
            {"type": 0,"coor": [2,1]},{"type": 1, "path": ['r'],"coor": [2,2]},{"type": 1, "path": ['l','t','b'],"coor": [2,3], "events": [enemy]},{"type": 0,"coor": [2,4]},{"type": 0,"coor": [2,5]},
            {"type": 0,"coor": [3,1]},{"type": 0,"coor": [3,2]},{"type": 1, "path": ['t','r','b'],"coor": [3,3]},{"type": 1, "path": ['l','r'],"coor": [3,4]},{"type": 1, "path": ['l', 'b'],"coor": [3,5]},
            {"type": 1,"path": ['r','b'],"coor": [4,1]},{"type": 1, "path": ['r','l'],"coor": [4,2]},{"type": 1, "path": ['t','b','l'],"coor": [4,3]},{"type": 0,"coor": [4,4]},{"type": 1, "path": ['t'],"coor": [4,5]},
            {"type": 1,"path": ['t','r'],"coor": [5,1]},{"type": 1, "path": ['r','l'],"coor": [5,2]},{"type": 1, "path": ['t','r','l'],"coor": [5,3]},{"type": 1, "path": ['l'],"coor": [5,4]},{"type": 0,"coor": [5,5]},
        ]
    room_num = 22
    return room_num, level_map


def leave_room(direction, map_level, map_user):
    pass


def enter_room(room_num, map_level, map_user):
    dif = 1
    room_level = map_level[room_num]
    room_user = map_user['rooms'][room_num]
    events = room_level.get('events', [])
    if room_user.get('new', True):
        if events:
            return events
        else:
            return [random_event(dif)]
    else:
        if events:
            events.insert(0, {'status': 'end'})
            # 塞入结束事件，handler判断为结束事件则准许用户移动。防止房间内的事件被自动触发
            return events

    return [{'status': 'end'}]


def random_event(dif):
    type_list = [{'type': 'enemy', 'weight': 2},
                 {'type': 'treasure', 'weight': 2},
                 {'type': 'incident', 'weight': 1},
                 {'type': 'nothing', 'weight': 3}]
    total_weight = 0
    for item in type_list:
        total_weight += item['weight']
        item['bound'] = total_weight
    if total_weight < 1:
        return
    rand = random.randint(1, total_weight)
    lower = 0
    event = 'nothing'
    for item in type_list:
        upper = item['bound']
        if lower < rand <= upper:
            event = item['type']
            break
        lower = upper
    if event == 'enemy':
        return generate_enemy(dif)
    elif event == 'treasure':
        return generate_treasure(dif)
    elif event == 'incident':
        return generate_effect(dif)
    elif event == 'nothing':
        return {"type": "message", "content": {"name": "message", "msg": "安全的房间"}}


def generate_enemy(dif):
    rand = random.randint(1, 4)
    lv = 1
    if rand > 2:
        lv = lv + 1
    return {
        "type": "enemy",
        "content": {
            "name": "enemy",
            "enemy": {
                "name": "MuyiShen"+str(rand),
                "lv": lv,
                "hp": (int(dif) + 2) * (5 + rand),
                "max_hp": (int(dif) + 2) * (5 + rand),
                "stamina": 2,
                "max_stamina": 2,
                "charge": 0,
                "attack": int(dif) + 2 + rand
            }
        },
        "result": {}
    }


def generate_boss(dif):
    return {
        "type": "enemy",
        "content": {
            "name": "enemy",
            "enemy": {
                "name": "LiYuan the Boss",
                "lv": 1,
                "hp": 40,
                "max_hp": 40,
                "stamina": 5,
                "max_stamina": 5,
                "charge": 0,
                "attack": 8
            }
        },
        "next":  {
            "type": "message",
            "content": {
                "name": "message",
                "msg": "你打败了Alpha版本的boss，恭喜你取得了胜利！",
            },
            "next": {
                "type": "journey_end",
                "journey": "win",
                "content": {
                    "name": "journey_end",
                    "journey": "win",
                },
            },
        }
    }


def generate_treasure(dif):
    result = random_effect(dif + 1)
    return {
        "type": "option",
        "content": {
            "name": "option",
            "msg": "你遇到一个宝箱，要怎么办呢(问号)",
            "options": [{"key": "a", "describe": "打开它"},
                        {"key": "b", "describe": "不管它"}]
        },
        "legalKeys": ["a", "b"],
        "results": {
            "a": result,
            "b": {},
        }
    }


def generate_effect(dif):
    result = random_effect(dif)
    return {
        "type": "message",
        "content": {
            "name": "message",
            "msg": "发生了意想不到的事情!",
        },
        "result": result,
    }


def random_effect(dif):
    rand = random.randint(0, 0)
    if rand == 0:
        number = random.randint(1, 5 * dif)
        return {"name": "damage", "point": number, "msg": "受到" + str(number) + "点伤害"}
    elif rand == 1:
        number = random.randint(3, 5 * dif)
        return {"name": "heal", "point": number, "msg": "恢复了" + str(number) + "点生命值"}
