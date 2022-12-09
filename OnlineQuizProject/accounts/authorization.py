from rest_framework import exceptions
from django.conf import settings
import jwt
from accounts import views
from django.shortcuts import render, redirect

def isAuthorized(request):
    token=request.session.get('Authorization')
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithm='HS256')
        username = payload['username']
        print(username,'user name')
        return payload['username']
    except:
        return None
        