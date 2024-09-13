import time
from Tg.tg import sedmsgs as send
from Tg.tg import cancelmsg
from flask import jsonify


def event(data, name, hsname, hschatid, chatid):
    '''
    事件处理
    '''
    pname = '事件中心'
    xh = 3600*8 #默认8个小时
    # 报警等级
    d_level = data['severity']
    # 订阅类型
    d_type = eval(data['subscription'])['conditions'][0]['value']
    # 策略名称
    d_name = data['strategyName']
    # 通知摘要
    zaiyao = eval(data['alert'])['meta']['sysEventMeta']['eventNameZh']

    # 主机名
    hostname = eval(data['alert'])['meta']['sysEventMeta']['instanceName']
    if hostname == '':
        print('跳过,没有主机名')
        return jsonify({'code': 200, 'info': '跳过,没有主机名'}), 200
    #产品
    product = eval(data['alert'])['meta']['sysEventMeta']['serviceTypeZh']
    # 时间
    c = data['startTime']
    # 将时间戳转为时间
    time_local = time.localtime(int(c) / 1000)
    # 将时间转为字符串
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    # 详情
    xq = eval(data['alert'])['eventContentMap']


    msg = """<b>阿里云【{}】报警</b>

[实例名称]: {}
[报警等级]: {}
[平台名称]: {}
[通知摘要]: {}
[产品]: {}
[订阅类型]: {}
[通知时间]: {}
[历史报警]: <a href="https://t.me/{}">历史报警记录</a>
[详情]: <pre>{}</pre>""".format(
    pname,
    hostname,
    d_level,
    d_name,
    zaiyao,
    product,
    d_type,
    dt,
    str(hsname),
    xq
)
    #消息发送
    res = send(msg, chat_id=chatid, ali_button=1, call_data='123', isFunc=1) #告警群
    send(msg, chat_id=hschatid)#历史群
    cancelmsg(msgid=str(res.message_id), chat_id=chatid, secodes=xh)