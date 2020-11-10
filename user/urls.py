from django.urls import path
from .views      import SignUpView, SignInView, KakaoSignInView

urlpatterns = [
    path('', SignUpView.as_view()), 
    path('/signin', SignInView.as_view()),
    path('/kakaosignin', KakaoSignInView.as_view()),
]

