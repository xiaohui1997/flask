from flask import Blueprint, request, jsonify
from Tg.tg import sedmsgs as send
from Tg.tg import cancelmsg, reply_to_message
import time
from Public.models import AliWebhook, AliWebhook_white, db
import uuid

alihook = Blueprint('alihook', __name__,
    static_folder='static', #静态文件夹
    template_folder='templates') #蓝图名称,导入的名称

@alihook.route("/aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/<string:name>/<string:chatid>/<string:hschatid>/<string:hsname>", methods=['POST']) #路径加密
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
        #处理数据
        try:
            # 处理黑名单
            print(AliWebhook_white.query.filter_by(instanceId=eval(data['dimensionsOriginal'])['instanceId'],
                                                   isall=1).first())
            print(AliWebhook_white.query.filter_by(rules=str(data['metricName'] + ' ' + data['expression']),
                                                   instanceId=eval(data['dimensionsOriginal'])['instanceId']).first())

            if AliWebhook_white.query.filter_by(instanceId=eval(data['dimensionsOriginal'])['instanceId'],
                                                isall=1).first():
                return jsonify({'code': 200, 'info': '已加入黑名单忽略全部报警消息'}), 200
            if AliWebhook_white.query.filter_by(rules=str(data['metricName'] + ' ' + data['expression']),
                                                instanceId=eval(data['dimensionsOriginal'])['instanceId']).first():
                return jsonify({'code': 200, 'info': '已加入黑名单忽略该规则报警消息'}), 200

            # 发生告警
            if data['alertState'] == 'ALERT':
                #ecs
                if data['metricProject']=="acs_ecs":
                    pname = 'ECS'
                    IP = data['instanceName'].split('/')[1]
                    link = "https://cloudmonitor.console.aliyun.com/productMonitorChart?category=ecs&dimension=instanceId%3A{}&region=all".format(eval(data['dimensionsOriginal'])['instanceId'])
                #rds
                elif data['metricProject']=="acs_rds":
                    pname = 'RDS'
                    IP = "无"
                    link = "https://rdsnext.console.aliyun.com/detail/{}/performance".format(eval(data['dimensionsOriginal'])['instanceId'])
                else:
                    return jsonify({'code': 200, 'info': '非报警消息'}), 403
                msg = """<b>阿里云{}报警:  {}</b>
    
[报警等级]: {}
[报警规则]:  {}
[报警持续时间]: {}
[实例名称]: {}
[实例IP]: {}
[当前数值]: {}
[所属平台]: {}
[监控图]: <a href="{}">查看监控图</a>
[历史报警]: <a href="https://t.me/{}">历史报警记录</a>
[通知发出时间]: {}
[原始数据]: <pre>{}</pre>
                """.format(
                        pname,
                        data['alertName'],
                        data['triggerLevel'],
                        data['metricName'] + ' ' + data['expression'].replace('<=', '&lt;=').replace('>=', '&gt;='),
                        data['lastTime'],
                        data['instanceName'].split('/')[0],
                        IP,
                        data['curValue'] + str(data['unit']),
                        str(name),
                        link,
                        str(hsname),
                        time.strftime("%Y-%m-%d %H:%M:%S",
                            time.localtime(
                            int(data['timestamp'][0:10]))),
                        str(eval(data['dimensionsOriginal']))
                )
                #消息发送
                #消息入库
                send(msg, chat_id=hschatid) #告警历史群
                res = send(msg, chat_id=chatid, ali_button=1, call_data=data['transId'], isFunc=1) #告警群
                new_webhook = AliWebhook(rules=str(data['metricName'] + ' ' + data['expression']), instanceId= eval(data['dimensionsOriginal'])['instanceId'], msgid=str(res.message_id), transId=data['transId'], timestamp=data['timestamp'])
                db.session.add(new_webhook)
                db.session.commit()
                return jsonify({'code': 200, 'info': '告警成功'}), 200
            #告警恢复
            elif data['alertState'] == 'OK':
                #ecs
                if data['metricProject']=="acs_ecs":
                    pname = 'ECS'
                    IP = data['instanceName'].split('/')[1]
                    link = "https://cloudmonitor.console.aliyun.com/productMonitorChart?category=ecs&dimension=instanceId%3A{}&region=all".format(eval(data['dimensionsOriginal'])['instanceId'])
                #rds
                elif data['metricProject']=="acs_rds":
                    pname = 'RDS'
                    IP = "无"
                    link = "https://rdsnext.console.aliyun.com/detail/{}/performance".format(eval(data['dimensionsOriginal'])['instanceId'])
                else:
                    return jsonify({'code': 200, 'info': '非报警消息'}), 403
                msg = """<b>阿里云{}报警【恢复】:  {}</b>
        
[当前状态]: {}
[所属平台]: {}
[实例名称]: {}
[实例IP]: {}
[当前数值]: {}
[报警规则]:  {}
[恢复时间]: {}
[持续时间]: {}
[监控图]: <a href="{}">查看监控图</a>
[历史报警]: <a href="https://t.me/{}">历史报警记录</a>
[原始数据]: <pre>{}</pre>
    """.format(
            pname,
            data['alertName'],
            data['triggerLevel'] + "😎",
            str(name), # str(name)
            data['instanceName'].split('/')[0],
            IP,
            data['curValue'] + str(data['unit']),
            data['metricName'] + ' ' + data['expression'].replace('<=', '&lt;=').replace('>=', '&gt;='),
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(
                              int(data['timestamp'][0:10]))),
            data['lastTime'],
            link,
            str(hsname),
            str(eval(data['dimensionsOriginal']))
        )
                #查出所有的msgid
                msgid_list = AliWebhook.query.with_entities(AliWebhook.msgid).filter_by(transId=data['transId']).order_by(AliWebhook.msgid.desc()).all()
                res = reply_to_message(chat_id=chatid, message_id=msgid_list[0][0], text=msg)
                #全部销毁
                for i in msgid_list:
                    cancelmsg(msgid=i[0], chat_id=chatid, secodes=20)#撤销告警通知(可能有多个,批量销毁)
                cancelmsg(msgid=str(res.message_id), chat_id=chatid, secodes=3600) #撤销回复默认1小时 3600秒
                send(msg, chat_id=hschatid) #告警历史群
                return jsonify({'code': 200, 'info': '告警成功'}), 200

            else:
                return jsonify({'code': 200, 'info': '非报警消息'}), 403
        except KeyError as e:
            # 走事件订阅渠道
            print('渠道')
            print(data['severity'])
            #订阅类型
            d_type = eval(data['subscription'])['conditions'][0]['value']
            print(d_type)
            return jsonify({'code': 200, 'info': 'successful'}), 200
    else:
        return 'Method not allowed'