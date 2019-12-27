from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from . import forms
from .models import Avatar
from Aeon_Citadel.models import Journey
from .validator.validator import init_avatar
import uuid
import json


@csrf_exempt
def create_avatar(request):
    success = False
    msg = ""
    if request.method == 'POST':
        avatar_form = forms.AvatarForm(request.POST)
        if avatar_form.is_valid():
            user_id = request.session['user_id']
            name = avatar_form.cleaned_data['name']
            attack = avatar_form.cleaned_data['attack']
            defense = avatar_form.cleaned_data['defense']
            speed = avatar_form.cleaned_data['speed']
            comment = avatar_form.cleaned_data['comment']
            skill_points = init_avatar({'atk': attack, 'def': defense, 'spe': speed})
            if skill_points < 0:
                return JsonResponse({"success": False, "msg": "输入的技能点有误"})
            avatar_id = uuid.uuid1()
            status = {"name": name, "hp": int(defense)*5, "max_hp": int(defense)*5, "defense": defense,
                      "attack": attack, "speed": speed, "exp": 0, "lv": 1, "max_stamina": speed, "stamina": speed,
                      "charge": 0, "skill_points": skill_points}
            status = json.dumps(status)
            new_avatar = Avatar.objects.create(avatar_id=avatar_id, user_id=user_id, name=name, attack=attack,
                                               defense=defense, speed=speed, comment=comment)
            new_journey = Journey.objects.create(avatar_id=avatar_id, avatar_name=name, avatar_status=status)
            new_avatar.save()
            new_journey.save()
            success = True
            msg = "创建成功"
        else:
            print(avatar_form.errors)
    return JsonResponse({"success": success, "msg": msg})


@csrf_exempt
def delete_avatar(request):
    success = False
    msg = ""
    if request.method == 'POST':
        avatar_id = request.POST['avatarId']
        avatar = Avatar.objects.filter(avatar_id=avatar_id)
        journey = Journey.objects.filter(avatar_id=avatar_id)
        if avatar and journey:
            Avatar.objects.filter(avatar_id=avatar_id).delete()
            Journey.objects.filter(avatar_id=avatar_id).delete()
            success = True
            msg = "删除成功"
        else:
            msg = "未找到该角色"
    return JsonResponse({"success": success, "msg": msg})


@csrf_exempt
def load_all_avatars(request):
    uid = request.session.get('user_id', None)
    data = Avatar.objects.filter(user_id=uid)
    avatar_list = []
    for avatar in data:
        avatar = model_to_dict(avatar)
        del avatar['user_id']
        avatar_list.append(avatar)
    return JsonResponse({"success": True, "msg": "", "avatars": avatar_list})


@csrf_exempt
def select_hero(request):
    if request.method == 'POST':
        avatar = request.POST['selectChar']
        query = Avatar.objects.values('user_id').filter(avatar_id=avatar)[0]
        if query['user_id'] == str(request.session.get('user_id', None)):
            request.session['selectChar'] = avatar
            return JsonResponse({"success": True, "msg": "something"})
        else:
            return JsonResponse({"success": False, "msg": "error"})
