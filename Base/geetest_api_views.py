import json

from SmartDjango import Analyse
from django.http import HttpResponse
# from django.shortcuts import render_to_response, RequestContext
from django.views import View
from geetest import GeetestLib
from smartify import P

geetest_id = "b1f425b289361afab1c3624e916a5b7d"  # 您的id, 在极验后台获取
geetest_key = "6891701a158938f1596941a000b7cfa0"  # 您的私钥, 在极验后台获取


class GetCaptchaView(View):
    @staticmethod
    def get(request):
        user_id = None
        gt = GeetestLib(geetest_id, geetest_key)
        status = gt.pre_process()
        request.session[gt.GT_STATUS_SESSION_KEY] = status
        request.session["user_id"] = user_id
        respone_str = gt.get_response_str()
        return HttpResponse(respone_str)



class ValidateView(View):
    @staticmethod
    def post(request):
        gt = GeetestLib(geetest_id, geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        return HttpResponse(result)


class AxiosValidateView(View):
    @staticmethod
    @Analyse.r(b=[P('geetest_challenge', 'challenge'), P('geetest_seccode', 'seccode'), P('geetest_validate', '验证码')])
    def post(request):
        gt = GeetestLib(geetest_id, geetest_key)
        challenge = request.d.geetest_challenge
        validate = request.d.geetest_validate
        seccode = request.d.geetest_seccode
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return HttpResponse(json.dumps(result))
