from django.http import JsonResponse


class AeonGlobalMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.find('login') or request.path.find('register'):
            return response
        if not request.session.get('is_login', None):
            return JsonResponse({"success": False, "msg": 'login required'})
        return response
