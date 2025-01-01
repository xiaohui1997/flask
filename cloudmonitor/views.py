from flask import Blueprint, request, jsonify
from .public.ALERT import alert, ok
from .public.event import event
import uuid

alihook = Blueprint('alihook', __name__,
    static_folder='static', #静态文件夹
    template_folder='templates') #蓝图名称,导入的名称

@alihook.route("/aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/<string:name>/<string:bot_token>/<string:secret>", methods=['POST', 'GET']) #路径加密
def aliyun_webhook(name, bot_token, secret):
    '''
    路径加密:固定
    平台名称: 可替换
    bot_token: lark机器人token
    secret: lark机器人secret
    完整路径: /aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/平台名称/bot_token/secret
    '''
    if request.method == 'GET':
        return jsonify({'code': 200, 'info': '请使用POST请求'}), 200
        
    ask = request.args.get('ask')  # 获取ak/sk 事件专用
    # 只接受 POST 请求
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        if data is None:
            info = {
                'code': 100001,
                'msg': '参数不完整'
            }
            return jsonify(info)
        
        # 事件订阅
        if 'severity' in data:
            res = event(data, name, bot_token, secret, ask)
            return res
        ################################################
        # 发生告警-告警处理
        elif 'alertState' in data and data['alertState'] == 'ALERT':
            # 通知告警
            res = alert(data, name, bot_token, secret)
            return res
        elif 'alertState' in data and data['alertState'] == 'OK':
            # 通知恢复
            res = ok(data, name, bot_token, secret)
            return res
        return jsonify({'code': 200, 'info': 'successful'}), 200
    else:
        return 'Method not allowed'
