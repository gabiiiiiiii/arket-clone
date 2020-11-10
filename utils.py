import json
import jwt

from django.views import View
from django.http  import JsonResponse
from user.models  import User
from aig.settings import SECRET_KEY, ALGORITHM

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            print(access_token)
            if access_token:
                token_paylod = jwt.decode(access_token, SECRET_KEY, algorithm = ALGORITHM)
                request.user = User.objects.get(email = token_paylod['email'])

                return func(self, request, *args, **kwargs)
            return JsonResponse({'MESSAGE':'LOGIN_REQUIRED'}, status = 401)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status = 400)
    return wrapper
