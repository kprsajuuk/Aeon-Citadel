from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .synchronizer.eventAction import handle_action
from django.forms.models import model_to_dict
from .models import Journey
# from Aeon_Avatar.models import Avatar


@csrf_exempt
def execute_action(request):
    if request.method == 'POST':
        avatar_id = request.session.get('selectChar', None)
        if not avatar_id:
            return JsonResponse({"success": False, "msg": "avatar error"})
        journey = model_to_dict(Journey.objects.filter(avatar_id=avatar_id)[0])
        event = request.session.get('event', None)
        action = request.POST['action_name']
        if not event:
            # noinspection PyBroadException
            try:
                event = eval(journey['event'])
            except Exception:
                event = ""
                pass
        # noinspection PyBroadException
        try:
            avatar = eval(journey['avatar_status'])
            difficulty = int(journey['difficulty'])
        except Exception:
            return JsonResponse({"success": False, "msg": "database error"})
        new_event, new_avatar = handle_action(event, action, avatar, difficulty)
        if not new_event:
            return JsonResponse({"success": False, "msg": "illegal request"})

        request.session['event'] = new_event
        Journey.objects.filter(avatar_id=avatar_id).update(event=new_event, avatar_status=new_avatar)
        return JsonResponse({"success": True, "msg": "", "event": new_event, "hero": new_avatar})

    return JsonResponse({"success": False, "msg": "error"})
