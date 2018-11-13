# chat/urls.py
from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth.views import (
    LoginView, logout_then_login,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
    )
from chatroom import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    path('register', views.register, name='register'),
    path('confirmEmail/<str:username>/<slug:token>/',views.confirmEmail, name = 'confirm'),
    path('login', LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout', logout_then_login, name='logout'),
    path('home',views.index, name='index'),
    path('invite_chat', views.invite_chat, name='invite_chat'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
