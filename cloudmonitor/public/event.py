import time, json, base64, re
from Public.lark_bot_send import send_message
from flask import jsonify
from Public.alibaba import Sample
from alibabacloud_sas20181203 import models as sas_20181203_models
from alibabacloud_tea_util import models as util_models


def login_ip(pname, hostname, d_level, d_name, zaiyao, product, uuids, unique_info, ask, region):
    # 解码
    decoded_bytes = base64.b64decode(ask)
    decoded_str = decoded_bytes.decode('utf-8')
    ak, sk = decoded_str.split('/')
    client = Sample(ak, sk, region).create_client()
    # 直接在这里定义请求参数
    describe_susp_events_request = sas_20181203_models.DescribeSuspEventsRequest(
        uuids=uuids,
        unique_info=unique_info
    )

    runtime = util_models.RuntimeOptions()

    # 调用API并处理返回值
    res = client.describe_susp_events_with_options(describe_susp_events_request, runtime).to_map()
    print(res)
    print('#'*30)
    # 事件名称
    re_name = res['body']['SuspEvents'][0]['AlarmEventNameDisplay']
    for i in res['body']['SuspEvents'][0]['Details']:
        if i['NameDisplay'] == '登录时间':
            re_time = i['Value']
        elif i['NameDisplay'] == '登录账号':
            re_user = i['Value']
        elif i['NameDisplay'] == '登录协议':
            re_type = i['Value']
        elif i['NameDisplay'] == '登录源IP':
            re_ip = i['Value']
        elif i['NameDisplay'] == '登录端口':
            re_port = i['Value']
        elif i['NameDisplay'] == '登录地':
            re_address = i['Value']
    msg = """[实例名称]: {}
[报警等级]: {}
[平台名称]: {}
[通知摘要]: {}
[产品]: {}
[描述]: {}
[登录时间]: {}
[登录账号]: {}
[登录协议]: {}
[登录源IP]: {}
[登录端口]: {}
[登录地点]: {}
[常用登录地管理]: <a href="https://yundun.console.aliyun.com/?spm=5176.12818093.console-base_search-panel.dtab-product_sas.269416d0s75WE2&p=sas#/ruleManagement/usualLogin/location/global">地区加白</a>
""".format(
        hostname,
        d_level,
        d_name,
        zaiyao,
        product,
        re_name,
        re_time,
        re_user,
        re_type,
        re_ip,
        re_port,
        re_address
    )
    return msg




def event(data, name, bot_token, secret, ask):
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

    #屏蔽部分消息
    if '磁盘快照' in zaiyao:
        return jsonify({'code': 200, 'info': '跳过,快照'}), 200
    if '资源标签' in zaiyao:
        return jsonify({'code': 200, 'info': '跳过,资源标签'}), 200

    #调试
    #print(data)

    msg = """[实例名称]: {}
[报警等级]: {}
[平台名称]: {}
[通知摘要]: {}
[产品]: {}
[订阅类型]: {}
[通知时间]: {}
[详情]: <pre>{}</pre>""".format(
    hostname,
    d_level,
    d_name,
    zaiyao,
    product,
    d_type,
    dt,
    xq
)
    # 拦截异常登录需额外处理
    if '异常登录' in zaiyao and ask != None:
        # 区域
        zone = eval(data['alert'])['arn']
        match = re.search(r'ecs:([^:]+):', zone)
        region = match.group(1)
        # uuids
        uuids = eval(data['alert'])['eventContentMap']['uuid']
        # unique_info
        unique_info = eval(data['alert'])['eventContentMap']['unique_info']
        msg = login_ip(pname, hostname, d_level, d_name, zaiyao, product, uuids, unique_info, ask, region)

    #消息发送
    title = "阿里云【{}】报警".format(pname)
    res = send_message(msg, title, bot_token, secret)  # 告警群
    print(res.text)
    return jsonify({'code': 200, 'info': 'successful'}), 200

if __name__ == '__main__':
    login_ip()
