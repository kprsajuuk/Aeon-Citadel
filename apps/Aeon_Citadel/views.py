from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .synchronizer.eventAction import update_journey


@csrf_exempt
def execute_action(request):
    if request.method == 'POST':
        avatar_id = request.session.get('selectChar', None)
        if not avatar_id:
            return JsonResponse({"success": False, "msg": "avatar error"})
        action = request.POST['action_name']
        success, data = update_journey(avatar_id, action)
        if not success:
            return JsonResponse({"success": False, "msg": "Action error"})
        else:
            return JsonResponse({"success": True, "msg": "", "data": data})

    return JsonResponse({"success": False, "msg": "error"})
