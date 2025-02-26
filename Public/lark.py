import hashlib
import base64
import hmac
import time
import json
import requests
from Public.config import FEISHU_CONFIG


FEISHU_CONFIG["secret"]


def gen_sign(timestamp, secret):
    """
    生成飞书机器人签名
    :param timestamp: 时间戳
    :param secret: 签名密钥
    :return: 签名字符串
    """
    # 拼接timestamp和secret
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign

def get_signed_params(secret):
    """
    获取带签名的基础参数
    :param secret: 签名密钥
    :return: 包含timestamp和sign的字典
    """
    timestamp = str(int(time.time()))
    sign = gen_sign(timestamp, secret)
    return {
        "timestamp": timestamp,
        "sign": sign
    } 

def send_message_alert(msg, pname, IP, link, hsname):
    """
    ecs告警
    """
    
    # 获取签名参数
    data = get_signed_params(FEISHU_CONFIG["secret"])
   

    data.update({
        "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": f"阿里云【{pname}】报警: {msg['alertName']}\n\n",
                "content": [
                    [
                        {"tag": "text", "text": "[报警等级]: "},
                        {"tag": "text", "text": f"{msg['triggerLevel']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[报警规则]: "},
                        {"tag": "text", "text": f"{msg['metricName']} {msg['expression']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[报警持续时间]: "},
                        {"tag": "text", "text": f"{msg['lastTime']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[实例名称]: "},
                        {"tag": "text", "text": f"{msg['instanceName'].split('/')[0]}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[实例IP]: "},
                        {"tag": "text", "text": f"{IP}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[当前数值]: "},
                        {"tag": "text", "text": f"{msg['curValue']} {msg['unit']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[所属平台]: "},
                        {"tag": "text", "text": f"TB"}
                    ],
                    [
                        {"tag": "text", "text": "[监控图]: "},
                        {"tag": "a", "text": "查看监控图", "href": link}
                    ],
                    [
                        {"tag": "text", "text": "[历史报警]: "},
                        {"tag": "a", "text": "历史报警记录", "href": f"https://t.me/{hsname}"}
                    ],
                    [
                        {"tag": "text", "text": "[原始数据]:\n"},
                        {"tag": "text", "text": str(eval(msg['dimensionsOriginal']))}
                    ]
                ]
            }
        }
    }
}
    )
    
    # 发送请求
    headers = {"Content-Type": "application/json"}
    response = requests.post(FEISHU_CONFIG["webhook_url"], headers=headers, data=json.dumps(data))
    return response

def send_message_recover(msg, pname, IP, link, hsname):
    """
    ecs告警
    """
    
    # 获取签名参数
    data = get_signed_params(FEISHU_CONFIG["secret"])
   

    data.update({
        "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": f"阿里云【{pname}】报警 【恢复】: {msg['alertName']}\n\n",
                "content": [
                    [
                        {"tag": "text", "text": "[当前状态]: "},
                        {"tag": "text", "text": f"{msg['triggerLevel']}😎\n"}
                    ],
                    [
                        {"tag": "text", "text": "[报警规则]: "},
                        {"tag": "text", "text": f"{msg['metricName']} {msg['expression']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[报警持续时间]: "},
                        {"tag": "text", "text": f"{msg['lastTime']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[实例名称]: "},
                        {"tag": "text", "text": f"{msg['instanceName'].split('/')[0]}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[实例IP]: "},
                        {"tag": "text", "text": f"{IP}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[当前数值]: "},
                        {"tag": "text", "text": f"{msg['curValue']} {msg['unit']}\n"}
                    ],
                    [
                        {"tag": "text", "text": "[所属平台]: "},
                        {"tag": "text", "text": f"TB"}
                    ],
                    [
                        {"tag": "text", "text": "[监控图]: "},
                        {"tag": "a", "text": "查看监控图", "href": link}
                    ],
                    [
                        {"tag": "text", "text": "[历史报警]: "},
                        {"tag": "a", "text": "历史报警记录", "href": f"https://t.me/{hsname}"}
                    ],
                    [
                        {"tag": "text", "text": "[原始数据]:\n"},
                        {"tag": "text", "text": str(eval(msg['dimensionsOriginal']))}
                    ]
                ]
            }
        }
    }
}
    )
    
    # 发送请求
    headers = {"Content-Type": "application/json"}
    response = requests.post(FEISHU_CONFIG["webhook_url"], headers=headers, data=json.dumps(data))
    return response