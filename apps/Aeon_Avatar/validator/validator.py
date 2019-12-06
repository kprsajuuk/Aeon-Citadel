from Aeon_Global import avatar_config


def init_avatar(attr):
    total = 0
    for key in attr:
        if int(attr[key]) >= 0:
            total += int(attr[key])
        else:
            return False
    if total <= avatar_config.init_point:
        return True
    else:
        return False
