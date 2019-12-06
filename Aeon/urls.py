"""Aeon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Aeon_Account import views as account
from Aeon_Avatar import views as avatar
from Aeon_Citadel import views as citadel

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account.login),
    path('logout/', account.logout),
    path('register/', account.register),
    path('createHero/', avatar.create_avatar),
    path('loadAllHero/', avatar.load_all_avatars),
    path('selectHero/', avatar.select_hero),
    path('takeAction/', citadel.execute_action),

    path('test/', citadel.test_func),
]
