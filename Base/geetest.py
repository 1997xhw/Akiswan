from _md5 import md5
import time

import requests
from pprint import pprint
import json


class Geetest:
    id = ""  # 您的id, 在极验后台获取
    key = ""  # 您的私钥, 在极验后台获取
    API_URL = "http://api.geetest.com/gt_verify"

    @staticmethod
    def verify(challenge, phone):
        seccode = md5((Geetest.key + challenge).encode()).hexdigest()
        query = {
            "id": id,
            "seccode": seccode,
            "idType": "1",
            "idValue": md5(phone.encode()).hexdigest(),
            "challenge": challenge,
            "user_ip": "1.2.3.4",
            "timestamp": time.time(),
            "crash": "0",
        }
        print("query:", query)
        resp = requests.post(Geetest.API_URL, data=query)
        print("response:", resp)
        result = resp.content
        print("result:", )
        pprint(json.loads(result.decode()))
        return result.json()['success']
