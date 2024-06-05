from flask import Blueprint, request, jsonify
from Tg.tg import sedmsgs as send

tg = Blueprint('tg', __name__,
    static_folder='static', #静态文件夹
    template_folder='templates') #蓝图名称,导入的名称


@tg.route("/sendmsg", methods=['POST'])
def sendmsg():
    start_token = '37aba484c6261fe79d9729d93a7084c4'
    # 只接受 POST 请求
    if request.method == 'POST':
        token = request.form.get('token')
        msg = request.form.get('msg')
        chatid = request.form.get('chatid')
        parse_mode = request.form.get('parse_type')

        if token is None or msg is None or chatid is None:
            info = {
                'code': 100001,
                'msg': '参数不完整'
            }
            return jsonify(info)
        #token校验
        if start_token != token:
            info = {
                'code': 100002,
                'msg': '403'
            }
            return jsonify(info)
        #消息发送
        try:
            if parse_mode is None:
                send(msg, chat_id=chatid)
            else:
                send(msg, parse_type=parse_mode, chat_id=chatid)
            return jsonify({'code': 200, 'info': '发送成功'})
        except Exception as e:
            return jsonify({'code': 100005, 'info': '请激活bot  run: /start', 'error': str(e)})
    else:
        return 'Method not allowed'