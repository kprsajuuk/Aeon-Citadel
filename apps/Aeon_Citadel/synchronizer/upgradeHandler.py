from django.forms.models import model_to_dict
from Aeon_Citadel.models import Journey


def upgrade_avatar(avatar_id, upgrade_type, upgrade_num):
    if upgrade_type and upgrade_num:
        journey = model_to_dict(Journey.objects.filter(avatar_id=avatar_id)[0])
        status = eval(journey['avatar_status'])
        points = int(status.get('skill_points', 0))
        if points > 0 and points >= upgrade_num:
            status['skill_points'] = points - upgrade_num
            if upgrade_type == 'attack':
                status['attack'] = int(status['attack']) + upgrade_num
            elif upgrade_type == 'defense':
                status['defense'] = int(status['defense']) + upgrade_num
                status['max_hp'] = 5 * int(status['defense'])
            elif upgrade_type == 'speed':
                status['speed'] = int(status['speed']) + upgrade_num
                status['max_stamina'] = int(status['speed'])
            else:
                return False
            Journey.objects.filter(avatar_id=avatar_id).update(avatar_status=status)
            return status
    return False



