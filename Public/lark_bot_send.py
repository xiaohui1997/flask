import json

import requests
import hashlib
import base64
import hmac
import time

timestamp = str(int(time.time()))
def gen_sign(secret):
    '''
    生成签名
    '''
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign


def send_message(message: str, title: str, bot_token: str, secret: str):
    url = "https://open.larksuite.com/open-apis/bot/v2/hook/{}".format(bot_token)
    data = {
        "timestamp": "{}".format(timestamp),
        "sign": "{}".format(gen_sign(secret)),
        "msg_type": "interactive",
        "card": {
            "elements": [{
                    "tag": "div",
                    "text": {
                            "content": "{}".format(message),
                            "tag": "lark_md"
                    }
            }, {
            }],
            "header": {
                    "title": {
                            "content": "{}".format(title),
                            "tag": "plain_text"
                    }
            }
        }
    }
    res = requests.post(url, data=json.dumps(data))
    return res

if __name__ == '__main__':
    send_message("hello", "我是标题","8d4f6e49-a79f-4f0a-b7b2-259725f7d9ef", "XD4OY1ki09K8FO655bNnN")