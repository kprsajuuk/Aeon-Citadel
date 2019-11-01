from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import forms
from . import models
import hashlib


@csrf_exempt
def login(request):
    if request.session.get('is_login', None):
        return JsonResponse({"success": False, "msg": '请勿重复登录'})
    message = ""
    success = False
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # noinspection PyBroadException
            try:
                user = models.User.objects.get(name=username)
                if user.password == md5_password(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    success = True
                    message = "登陆成功"
                else:
                    message = "密码错误"
            except Exception as e:
                print(e)
                message = "用户不存在"
                pass
    return JsonResponse({"success": success, "msg": message})


@csrf_exempt
def register(request):
    if request.session.get('is_login', None):
        return JsonResponse({"success": False, "msg": "已登录，请先退出登录"})
    message = ""
    success = False
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            confirm_password = register_form.cleaned_data['confirm_password']
            if password != confirm_password:
                message = "两次密码不一样"
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户已存在"
                else:
                    new_user = models.User.objects.create()
                    new_user.name = username
                    new_user.password = md5_password(password)
                    new_user.save()
                    success = True
                    message = "注册成功"
    return JsonResponse({"success": success, "msg": message})


@csrf_exempt
def logout(request):
    if not request.session.get('is_login', None):
        return JsonResponse({"success": False, "msg": '并未登录'})
    #del request.session['is_login']
    #del request.session['user_id']
    #del request.session['user_name']
    #del request.session['event']
    request.session.flush()
    return JsonResponse({"success": True, "msg": '成功退出登录'})


def md5_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result
