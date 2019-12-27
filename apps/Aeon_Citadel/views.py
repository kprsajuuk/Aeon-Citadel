from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .synchronizer.eventAction import ActionHandler
from .synchronizer.upgradeHandler import upgrade_avatar
from . import forms


@csrf_exempt
def execute_action(request):
    if request.method == 'POST':
        avatar_id = request.session.get('selectChar', None)
        if not avatar_id:
            return JsonResponse({"success": False, "msg": "avatar error"})
        action = request.POST['action_name']
        action_handler = ActionHandler(avatar_id, action)
        success, data = action_handler.handle_journey()
        if not success:
            return JsonResponse({"success": False, "msg": "Action error"})
        else:
            return JsonResponse({"success": True, "msg": "", "data": data})

    return JsonResponse({"success": False, "msg": "error"})


@csrf_exempt
def upgrade_status(request):
    if request.method == 'POST':
        avatar_id = request.session.get('selectChar', None)
        if not avatar_id:
            return JsonResponse({"success": False, "msg": "avatar error"})
        upgrade_form = forms.UpgradeForm(request.POST)
        if upgrade_form.is_valid():
            upgrade_type = upgrade_form.cleaned_data['type']
            upgrade_num = upgrade_form.cleaned_data['num']
            avatar = upgrade_avatar(avatar_id, upgrade_type, upgrade_num)
            if not avatar:
                return JsonResponse({"success": False, "msg": "update fail"})
            else:
                return JsonResponse({"success": True, "hero": avatar, "msg": "update success"})
    return JsonResponse({"success": False, "msg": "error"})


def test_func(request):
    from .synchronizer.room.room_generator import random_event
    dlist = []
    for i in range(30):
        dlist.append(random_event(10))
    return JsonResponse({"success": True, "msg": "sth", "data": dlist})
