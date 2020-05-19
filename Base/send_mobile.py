from Base.session import Session
from urllib.parse import urlencode
from django.utils.crypto import get_random_string
import requests
import json

yunpian_appkey = "17b6380427edbd4d923165321bb40b38"


# 之后记得塞进config里面隐藏起来！！！！


class SendMobile:
    texts = '【Akiiita】本次注册的验证码为#code#，五分钟内有效。'
    PHONE = 'phone'
    PHONE_NUMBER = 'phone_number'

    @staticmethod
    def send_captcha(request, mobile):
        text = SendMobile.texts
        code = get_random_string(length=6, allowed_chars="1234567890")
        text = text.replace("#code#", code)

        SendMobile._send_sms(yunpian_appkey, text, mobile)
        Session.save_captcha(request, SendMobile.PHONE, code)
        Session.save(request, SendMobile.PHONE_NUMBER, mobile)

    @staticmethod
    def check_captcha(request, code):
        Session.check_captcha(request, SendMobile.PHONE, code)
        phone = Session.load(request, SendMobile.PHONE_NUMBER)
        return phone

    @staticmethod
    def _send_sms(apikey, text, mobile):
        """
        云片短信发送API
        :param apikey: 云片应用密钥
        :param text: 发送明文
        :param mobile: 11位手机号
        :return:
        """
        # 服务地址
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        params = urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        response = requests.post(url, params, headers=headers)
        response_str = response.text
        response.close()
        return json.loads(response_str)
