from flask import jsonify
import time
from Public.lark_bot_send import send_message


def alert(data, name, bot_token, secret):
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
    else:
        return jsonify({'code': 200, 'info': '非报警消息'}), 403

#######################################上面条件判断########################################

    msg = """[报警等级]: {}
[报警规则]:  {}
[报警持续时间]: {}
[实例名称]: {}
[实例IP]: {}
[当前数值]: {}
[所属平台]: {}
[监控图]: <a href="{}">查看监控图</a>
[通知发出时间]: {}
[原始数据]: <pre>{}</pre>
                    """.format(
        data['triggerLevel'],
        data['metricName'] + ' ' + data['expression'].replace('<=', '&lt;=').replace('>=', '&gt;='),
        data['lastTime'],
        data['instanceName'].split('/')[0],
        IP,
        data['curValue'] + str(data['unit']),
        str(name),
        link,
        time.strftime("%Y-%m-%d %H:%M:%S",
                      time.localtime(
                          int(data['timestamp'][0:10]))),
        str(eval(data['dimensionsOriginal']))
    )
    print(msg)
    # 消息发送
    title = "阿里云【{}】报警:  {}".format(pname, data['alertName'])
    res = send_message(msg, title,bot_token, secret)  # 告警群
    print(res.text)
    return jsonify({'code': 200, 'info': '告警成功'}), 200


#######################################上面告警发送########################################


def ok(data, name, bot_token, secret):
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
    else:
        return jsonify({'code': 200, 'info': '非报警消息'}), 403

    #######################################上面条件判断########################################

    msg = """[当前状态]: {}
[所属平台]: {}
[实例名称]: {}
[实例IP]: {}
[当前数值]: {}
[报警规则]:  {}
[恢复时间]: {}
[持续时间]: {}
[监控图]: <a href="{}">查看监控图</a>
[原始数据]: <pre>{}</pre>
            """.format(
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
        str(eval(data['dimensionsOriginal']))
    )
    # 恢复消息发送
    title = "阿里云【{}】报警:  {}".format(pname, data['alertName'])
    res = send_message(msg, title, bot_token, secret)  # 告警群
    print(res.text)
    return jsonify({'code': 200, 'info': '告警恢复成功'}), 200