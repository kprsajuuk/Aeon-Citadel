from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from . import forms
from .models import Avatar
from Aeon_Citadel.models import Journey
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
            a_range = avatar_form.cleaned_data['range']
            magic = avatar_form.cleaned_data['magic']
            comment = avatar_form.cleaned_data['comment']
            avatar_id = uuid.uuid1()
            status = {"name": name, "hp": 100, "max_hp": 100, "attack": 50, "exp": 0, "lv": 1, "speed": speed}
            status = json.dumps(status)
            new_avatar = Avatar.objects.create(avatar_id=avatar_id, user_id=user_id, name=name, attack=attack,
                                               defense=defense, speed=speed, range=a_range, magic=magic,
                                               comment=comment)
            new_journey = Journey.objects.create(avatar_id=avatar_id, avatar_name=name, avatar_status=status)
            new_avatar.save()
            new_journey.save()
            success = True
            msg = "创建成功"
        else:
            print(avatar_form.errors)
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
