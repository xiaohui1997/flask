from flask import Blueprint, request, jsonify
from .public.ALERT import alert, ok
from .public.event import event
import uuid

alihook = Blueprint('alihook', __name__,
    static_folder='static', #静态文件夹
    template_folder='templates') #蓝图名称,导入的名称

@alihook.route("/aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/<string:name>/<string:chatid>/<string:hschatid>/<string:hsname>", methods=['POST', 'GET']) #路径加密
def aliyun_webhook(name, chatid, hschatid, hsname):
    '''
    路径加密:固定
    平台名称: 可替换
    chat_id: 可替换
    hschatid: 历史群组id
    hsname: 历史群组名称,分享链接名称：+KhBOVqnJjswzOTE0
    完整路径: /aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/平台名称/chat_id
    '''
    if request.method == 'GET':
        return jsonify({'code': 200, 'info': '请使用POST请求'}), 200

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
            event(data, name, hsname, hschatid, chatid)
        ################################################
        # 发生告警-告警处理
        if data['alertState'] == 'ALERT':
            # 通知告警
            alert(data, name, hsname, hschatid, chatid)
        elif data['alertState'] == 'OK':
            # 通知恢复
            ok(data, name, hsname, hschatid, chatid)
        return jsonify({'code': 200, 'info': 'successful'}), 200
    else:
        return 'Method not allowed'