from django.http import JsonResponse
from . import forms
from . import models


def login(request):
    print("first connection in this universe...")
    message = "hi"
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            #  noinspection PyBroadException
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    return True
                else:
                    message = "密码错误"
            except Exception:
                message = "用户不存在"
                pass
        return JsonResponse({"success": True, "err": message})
    else:
        return JsonResponse({"success": False, "err": message})
