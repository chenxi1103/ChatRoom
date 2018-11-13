from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.utils.safestring import mark_safe
import json
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from chat.models import *
from chat.forms import *

@transaction.atomic
def register(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'chat/register.html', context)
    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'chat/register.html', context)
    try:
        new_user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],)
        new_user.is_active = 0
        new_user.save()
        token = default_token_generator.make_token(new_user)
        email_body = """
            I am waiting for you for a long time! So great to see you here!
            Welcome to ChatRoom (￣∇￣) There is only one last step to be our member!
            Simply click this link and enjoy~
            http://%s%s
        """ % (request.get_host(),
               reverse('confirm', args=(new_user.username, token)))
        send_mail(
            subject='Welcome to ChatRoom! One more step: Verify your email adress!',
            message=email_body,
            from_email='chenxili@andrew.cmu.edu',
            recipient_list=[new_user.email]
            )
        new_userProfile = userProfile.objects.create(user=new_user,
                                                     email=
                                                     form.cleaned_data[
                                                         'email'],
                                                     )
        new_userProfile.save()
        return render(request, 'chat/emailConfirm.html')
    except:
        return render(request, 'chat/register.html', {
            'error': 'Sorry! The username is registered! Try another one!'})


@transaction.atomic
def confirmEmail(request, username, token):
    confirmUser = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(confirmUser, token):
        raise Http404
    confirmUser.is_active = True
    confirmUser.save()
    return render(request, 'chat/confrim_email_complete.html')

@login_required
def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'currUser': request.user,
        'roomname': room_name
    })

@login_required
def invite_chat(request):
    try:
        if request.method == 'POST':
            roomname = request.POST['roomname']
            friend = request.POST['friend']
            invited_user = User.objects.get(username=friend)
            email_body = """
                        Greetings from ChatRoom (｡･ω･｡)ﾉ
                        The user "%s" wants to invite you for chatting in room <%s>. Please click 
                        the following link if you want to accept the invitation:
                        http://%s/chat/%s
                        """ % (request.user.username, roomname, request.get_host(), roomname)
            send_mail(
                    subject='%s invite you for chatting!' %(request.user.username),
                    message=email_body,
                    from_email='chenxili@andrew.cmu.edu',
                    recipient_list=[invited_user.email]
                 )
            return room(request,roomname)
        else:
            return render(request, "chat/index.html",{})
    except:
        return render(request,"chat/index.html",{'error':"Sorry! This user does not exist! Try another one!"})
