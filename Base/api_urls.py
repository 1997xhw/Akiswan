""" Adel Liu 180301

base子路由
"""
from django.urls import path

from Base.api_views import ErrorView
from Base.geetest_api_views import GetCaptchaView, ValidateView, AxiosValidateView

urlpatterns = [
    path('errors', ErrorView.as_view()),
    path('geetest/getcaptcha', GetCaptchaView.as_view()),
    path('geetest/validate', ValidateView.as_view()),
    path('geetest/axiosvalidate', AxiosValidateView.as_view()),

]
