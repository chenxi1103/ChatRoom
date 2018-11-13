#!/usr/bin/env python
# coding:utf-8
# ------Author:Chenxi Li--------

from django.contrib.auth.models import User
from django.db import models

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30,)
    follower = models.ManyToManyField(User, related_name='followed',
                                    symmetrical=False)
    def __str__(self):
        return self.user
