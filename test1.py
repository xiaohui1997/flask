data = {'severity': 'INFO', 'userInfo': '{"aliyunId":"xinbo5988@gmail.com","userIdSec":"520546***45164","aliyunIdSec":"xinbo59***il.com","nickName":"xinbo5988","nickNameSec":"xin***988","userName":"TRẦN NHÂNTẠO","userId":"5205465841845164","userNameSec":"TRẦN***NTẠO"}', 'strategyName': '测试', 'relatedAlertIds': '["1e944627-80d9-4386-a87c-3b34bbf44763"]', 'groupingId': '8e89fb894cdb4430b2b6ede761820118', 'project': 'acs_custom_5205465841845164', 'retriggerTime': '0', 'subscription': '{"subscriptionUuid":"f2a391f18e6a46f8b664ef2d35f21d2c","conditions":[{"op":"EQ","field":"source","value":"SYS_EVENT"}],"relation":"AND"}', 'batchId': '6d8229b3a0c64fd2a1546cc0003637bb', 'userId': '5205465841845164', 'escalationLevel': '0', 'alert': '{"alertStatus":"TRIGGERED","traceId":"1e944627-80d9-4386-a87c-3b34bbf44763","severity":"INFO","product":"ECS","groupId":"239356893","eventRawContent":"{\\"resourceId\\":\\"i-0xidg1uxr1ii3b1wvvl1\\",\\"publicIpAddress\\":\\"47.253.108.138\\",\\"instanceName\\":\\"us-fanye-test-web\\",\\"instanceType\\":\\"ecs.g7.large\\",\\"state\\":\\"Stopping\\",\\"privateIpAddress\\":\\"10.20.20.214\\",\\"resourceType\\":\\"ALIYUN::ECS::Instance\\"}","project":"acs_custom_5205465841845164","source":"SYS_EVENT","eventType":"StatusNotification","userId":"5205465841845164","groupName":"test","eventContentMap":{"resourceId":"i-0xidg1uxr1ii3b1wvvl1","publicIpAddress":"47.253.108.138","instanceName":"us-fanye-test-web","instanceType":"ecs.g7.large","state":"Stopping","privateIpAddress":"10.20.20.214","resourceType":"ALIYUN::ECS::Instance"},"meta":{"sysEventMeta":{"regionNameEn":"us-east-1","resourceId":"acs:ecs:us-east-1:5205465841845164:instance/i-0xidg1uxr1ii3b1wvvl1","product":"ECS","eventNameEn":"Instance:StateChange","instanceName":"us-fanye-test-web","level":"INFO","resource":"","regionNameZh":"美东弗吉尼亚","groupId":"239356893","serviceTypeEn":"ECS","eventType":"StatusNotification","serviceTypeZh":"云服务器ECS","regionId":"us-east-1","eventTime":"20240910T172637.108+0800","name":"Instance:StateChange","id":"1e944627-80d9-4386-a87c-3b34bbf44763","status":"Normal","eventNameZh":"实例状态改变通知"}},"dedupId":"1e944627-80d9-4386-a87c-3b34bbf44763","eventName":"Instance:StateChange","arn":"acs:ecs:us-east-1:5205465841845164:instance/i-0xidg1uxr1ii3b1wvvl1","timestamp":1725960397000}', 'alertCount': '0', 'nextEscalateTime': '0', 'startTime': '1725960397000', 'time': '1725960397000', 'autoResolveTime': '0'}


try:
    if data['alertState'] == 'ALERT':
        # ecs
        print(123123)
        pass
    # rds
    elif data['metricProject'] == "acs_rds":
        pass
    else:
        pass
except KeyError as e:
    #走事件订阅渠道
    a = eval(data['subscription'])
    print(a['conditions'][0]['value'])
    print(data['severity'])