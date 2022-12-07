from rest_framework import exceptions
from django.conf import settings
import jwt
def isAuthorized(request):
    token=request.session.get('Authorization')
    if token:
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithm='HS256')
            username = payload['username']
            print(username,'user name')
            return payload['username']
        except:
            raise exceptions.AuthenticationFailed('unauthenticated!')