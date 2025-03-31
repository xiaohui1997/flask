from flask import Blueprint, request, jsonify
from Tg.tg import sedmsgs as send
import time
from Public.models import AliWebhook, AliWebhook_white, db
from Tg.tg import cancelmsg, reply_to_message
from Public.lark import send_message_alert, send_message_recover

def alert(data, name, hsname, hschatid, chatid):
    '''
    告警处理函数
    '''
    # ecs
    if data['metricProject'] == "acs_ecs":
        pname = 'ECS'
        IP = data['instanceName'].split('/')[1]
        link = "https://cloudmonitor.console.aliyun.com/productMonitorChart?category=ecs&dimension=instanceId%3A{}&region=all".format(
            eval(data['dimensionsOriginal'])['instanceId'])

    # rds
    elif data['metricProject'] == "acs_rds":
        pname = 'RDS'
        IP = "无"
        link = "https://rdsnext.console.aliyun.com/detail/{}/performance".format(
            eval(data['dimensionsOriginal'])['instanceId'])
    #redis-cluster
    elif data['metricProject'] == "acs_kvstore":
        print(data['regionId'])
        pname = 'Redis-cluster'
        IP = "无"
        link = "https://kvstore.console.aliyun.com/Redis/instance/{}/{}".format(
            str(data['regionId']), eval(data['dimensionsOriginal'])['instanceId'])

    #多指标处理
    elif data['metricName'] == "多指标":
        pname = data['metricProject']
        IP = "无"
        link = "https://cloudmonitor.console.aliyun.com"
        data['curValue'] = ''
        data['unit'] = ''
    else:
        #通用消息处理
        try:
            pname = data['metricProject']
            IP = "无"
            link = "https://cloudmonitor.console.aliyun.com"
        except Exception as e:
            print(e)
            print('触发异常')
            return jsonify({'code': 200, 'info': '非报警消息'}), 403

#######################################上面条件判断########################################

    msg = """<b>阿里云【{}】报警:  {}</b>

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
    print(msg)
    exit()
    # 消息发送
    send(msg, chat_id=chatid)  # 告警群
    send(msg, chat_id=hschatid)  # 告警历史群
    if name == 'TB':
        send_message_alert(data, pname, IP, link, hsname) #lg lark
    # 消息入库
    #new_webhook = AliWebhook(rules=str(data['metricName'] + ' ' + data['expression']),
    #                         instanceId=eval(data['dimensionsOriginal'])['instanceId'], msgid=str(res.message_id),
    #                         transId=data['transId'], timestamp=data['timestamp'])
    #db.session.add(new_webhook)
    #db.session.commit()
    return jsonify({'code': 200, 'info': '告警成功'}), 200


#######################################上面告警发送########################################


def ok(data, name, hsname, hschatid, chatid):
    '''
    告警恢复处理函数
    '''
    #消息销毁时间-8小时
    xh=3600*8
    # ecs
    if data['metricProject'] == "acs_ecs":
        pname = 'ECS'
        IP = data['instanceName'].split('/')[1]
        link = "https://cloudmonitor.console.aliyun.com/productMonitorChart?category=ecs&dimension=instanceId%3A{}&region=all".format(
            eval(data['dimensionsOriginal'])['instanceId'])

    # rds
    elif data['metricProject'] == "acs_rds":
        pname = 'RDS'
        IP = "无"
        link = "https://rdsnext.console.aliyun.com/detail/{}/performance".format(
            eval(data['dimensionsOriginal'])['instanceId'])
    # 多指标处理
    elif data['metricName'] == "多指标":
        pname = data['metricProject']
        IP = "无"
        link = "https://cloudmonitor.console.aliyun.com"
        data['curValue'] = ''
        data['unit'] = ''
    else:
        # 通用消息处理
        try:
            pname = data['metricProject']
            IP = "无"
            link = "https://cloudmonitor.console.aliyun.com"
        except Exception as e:
            print(e)
            print('触发异常')
            return jsonify({'code': 200, 'info': '非报警消息'}), 403

    #######################################上面条件判断########################################

    msg = """<b>阿里云【{}】报警【恢复】:  {}</b>

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
        str(name),  # str(name)
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
    # 查出告警的msgid
    #msgid_list = AliWebhook.query.with_entities(AliWebhook.msgid).filter_by(transId=data['transId']).order_by(
    #    AliWebhook.msgid.desc()).all()
    # 恢复消息发送
    #try:
    #    res = reply_to_message(chat_id=chatid, message_id=msgid_list[0][0], text=msg)# 告警群
    ##    for i in msgid_list:
    #        cancelmsg(msgid=i[0], chat_id=chatid, secodes=20)  # 撤销告警通知(可能有多个,批量销毁)
    #    cancelmsg(msgid=str(res.message_id), chat_id=chatid, secodes=xh)  # 撤销回复
    #    send(msg, chat_id=hschatid)  # 告警历史群
    #except Exception as e:
        #print('触发异常')
        #print(e)
        #send(msg, chat_id=chatid, ali_button=1, call_data=data['transId'], isFunc=1)  # 告警群
    send(msg, chat_id=chatid)  # 告警群
    send(msg, chat_id=hschatid) # 告警历史群
    if name == 'TB':
        send_message_recover(data, pname, IP, link, hsname) #lg lark
    return jsonify({'code': 200, 'info': '告警恢复成功'}), 200