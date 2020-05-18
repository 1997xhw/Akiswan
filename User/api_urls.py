from django.urls import path
from User.api_views import UserView, UsernameView, TokenView, SendRegisterCaptchaView

urlpatterns = [
    path('', UserView.as_view()),
    path('/@<str:username>', UsernameView.as_view()),
    path('/token', TokenView.as_view()),
    path('/registerCaptcha', SendRegisterCaptchaView.as_view())
]
