import re
import json
import jwt
import requests
import bcrypt

from django.views import View
from django.http  import JsonResponse

from .models      import User
from aig.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message' : 'EXISTS_EMAIL'}, status = 400)
            if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,25}$', data['password']):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            
            User.objects.create(
                email    = data['email'],
                password = hashed_password.decode('utf-8'),
                country  = data['country'],
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'email':user.email}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
                    return JsonResponse({'access_token' : token}, status = 200)
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class KakaoSignInView(View):
    def post(self, request):
        access_token    = request.headers.get('Authorization')
        profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers= {"Authorization" : f"Bearer {access_token}"}).json()
        kakao_account   = profile_request.get('kakao_account')
        email           = kakao_account.get('email',None)
        if User.objects.filter(email=email).exists():
            user  = User.objects.get(email=email)
            access_token = jwt.encode({'email':user.email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')

            return JsonResponse({'access_token'  : access_token, 'message' : 'SUCCESS'}, status=200)
        else:
            user = User.objects.create(
                email = email
            )              
            access_token = jwt.encode({'email':user.email}, SECRET_KEY, algorithm=ALGORITHM).decode('utf-8')

            return JsonResponse({'access_token'  : access_token, 'message' : 'SUCCESS'}, status=200)
