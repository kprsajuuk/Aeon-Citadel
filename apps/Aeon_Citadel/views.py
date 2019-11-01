from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .synchronizer.eventAction import handle_action


@csrf_exempt
def execute_action(request):
    if request.method == 'POST':
        event = request.session.get('event', None)
        action = request.POST['action_name']
        new_event = handle_action(event, action)
        if not new_event:
            return JsonResponse({"success": False, "msg": "illegal request"})
        request.session['event'] = new_event
        return JsonResponse({"success": True, "msg": "", "event": new_event})

    return JsonResponse({"success": False, "msg": "error"})
