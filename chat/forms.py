#!/usr/bin/env python
# coding:utf-8
# ------Author:Chenxi Li--------
from django import forms
from .models import userProfile
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput())
    email = forms.EmailField(max_length=100, label='email')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if userProfile.objects.filter(email__exact=email):
            raise forms.ValidationError("This Email has already registered!")
        return email