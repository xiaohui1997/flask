import requests
a={'severity': 'INFO1', 'userInfo': '{"aliyunId":"xinbo5988@gmail.com","userIdSec":"520546***45164","aliyunIdSec":"xinbo59***il.com","nickName":"xinbo5988","nickNameSec":"xin***988","userName":"TRẦN NHÂNTẠO","userId":"5205465841845164","userNameSec":"TRẦN***NTẠO"}', 'strategyName': '测试', 'relatedAlertIds': '["b28cecde-873c-478a-95fc-372c5a44f425"]', 'groupingId': '8e89fb894cdb4430b2b6ede761820118', 'project': 'acs_custom_5205465841845164', 'retriggerTime': '0', 'subscription': '{"subscriptionUuid":"f2a391f18e6a46f8b664ef2d35f21d2c","conditions":[{"op":"EQ","field":"source","value":"SYS_EVENT"}],"relation":"AND"}', 'batchId': '13d9d535f89a48a7a2b66d4d3f5549a5', 'userId': '5205465841845164', 'escalationLevel': '0', 'alert': '{"alertStatus":"TRIGGERED","traceId":"b28cecde-873c-478a-95fc-372c5a44f425","severity":"INFO","product":"ECS","groupId":"239356893","eventRawContent":"{\\"resourceId\\":\\"i-0xidg1uxr1ii3b1wvvl1\\",\\"publicIpAddress\\":\\"47.253.108.138\\",\\"instanceName\\":\\"us-fanye-test-web\\",\\"instanceType\\":\\"ecs.g7.large\\",\\"state\\":\\"Stopping\\",\\"privateIpAddress\\":\\"10.20.20.214\\",\\"resourceType\\":\\"ALIYUN::ECS::Instance\\"}","project":"acs_custom_5205465841845164","source":"SYS_EVENT","eventType":"StatusNotification","userId":"5205465841845164","groupName":"test","eventContentMap":{"resourceId":"i-0xidg1uxr1ii3b1wvvl1","publicIpAddress":"47.253.108.138","instanceName":"us-fanye-test-web","instanceType":"ecs.g7.large","state":"Stopping","privateIpAddress":"10.20.20.214","resourceType":"ALIYUN::ECS::Instance"},"meta":{"sysEventMeta":{"regionNameEn":"us-east-1","resourceId":"acs:ecs:us-east-1:5205465841845164:instance/i-0xidg1uxr1ii3b1wvvl1","product":"ECS","eventNameEn":"Instance:StateChange","instanceName":"us-fanye-test-web","level":"INFO","resource":"","regionNameZh":"美东弗吉尼亚","groupId":"239356893","serviceTypeEn":"ECS","eventType":"StatusNotification","serviceTypeZh":"云服务器ECS","regionId":"us-east-1","eventTime":"20240912T173929.172+0800","name":"Instance:StateChange","id":"b28cecde-873c-478a-95fc-372c5a44f425","status":"Normal","eventNameZh":"实例状态改变通知"}},"dedupId":"b28cecde-873c-478a-95fc-372c5a44f425","eventName":"Instance:StateChange","arn":"acs:ecs:us-east-1:5205465841845164:instance/i-0xidg1uxr1ii3b1wvvl1","timestamp":1726133969000}', 'alertCount': '0', 'nextEscalateTime': '0', 'startTime': '1726133969000', 'time': '1726133969000', 'autoResolveTime': '0'}
a={'severity': 'INFO', 'userInfo': '{"aliyunId":"wokar490@gmail.com","userIdSec":"550739***61872","aliyunIdSec":"wokar4***il.com","nickName":"wokar490","nickNameSec":"wok***90","userName":"QUOC NAMNGUYEN","userId":"5507393815461872","userNameSec":"QUOC ***UYEN"}', 'strategyName': 'wallet', 'relatedAlertIds': '["202c9fd4-4759-4609-bfd6-6fc1c4246b33"]', 'groupingId': 'fa3f262e0e7640eda3a80d718a15e786', 'project': 'acs_custom_5507393815461872', 'retriggerTime': '0', 'subscription': '{"times":5,"periodMin":5,"subscriptionUuid":"4e663eb013374a069b06484b2380fd22","silenceSec":300,"conditions":[{"op":"EQ","field":"source","value":"SYS_EVENT"},{"op":"INTERSECT","field":"groupId","value":"239355152,239355674,239355929"}],"relation":"AND"}', 'batchId': '2d357118d17546ca851911992402152e', 'userId': '5507393815461872', 'escalationLevel': '0', 'alert': '{"alertStatus":"TRIGGERED","traceId":"202c9fd4-4759-4609-bfd6-6fc1c4246b33","severity":"INFO","product":"Config","groupId":"239355152","eventRawContent":"{\\"configurationDiffs\\":[{\\"changeProperty\\":\\"InstanceName\\",\\"newPropertyValue\\":\\"arb-prod-app4_销毁\\",\\"oldPropertyValue\\":\\"arb-prod-app4\\"}],\\"resourceId\\":\\"i-t4n5t2ro5em52kfn4mha\\",\\"resourceType\\":\\"ACS::ECS::Instance\\",\\"tags\\":\\"{\\\\\\"acs:tag:createdby\\\\\\":[\\\\\\"sub:216971399956305692:felix\\\\\\"]}\\"}","project":"acs_custom_5507393815461872","source":"SYS_EVENT","eventType":"Notification","userId":"5507393815461872","groupName":"ARB","eventContentMap":{"resourceId":"i-t4n5t2ro5em52kfn4mha","configurationDiffs":[{"newPropertyValue":"arb-prod-app4_销毁","changeProperty":"InstanceName","oldPropertyValue":"arb-prod-app4"}],"resourceType":"ACS::ECS::Instance","tags":"{\\"acs:tag:createdby\\":[\\"sub:216971399956305692:felix\\"]}"},"meta":{"sysEventMeta":{"regionNameEn":"ap-southeast-1","resourceId":"acs:ecs:ap-southeast-1:5507393815461872:instance/i-t4n5t2ro5em52kfn4mha","product":"Config","eventNameEn":"ConfigurationItemChangeNotification","instanceName":"arb-prod-app4_销毁","level":"INFO","resource":"","regionNameZh":"新加坡","groupId":"239355152","serviceTypeEn":"Config","eventType":"Notification","serviceTypeZh":"Config","regionId":"ap-southeast-1","eventTime":"20240912T192553.355+0800","name":"ConfigurationItemChangeNotification","id":"202c9fd4-4759-4609-bfd6-6fc1c4246b33","status":"normal","eventNameZh":"配置项变更"}},"dedupId":"202c9fd4-4759-4609-bfd6-6fc1c4246b33","eventName":"ConfigurationItemChangeNotification","arn":"acs:ecs:ap-southeast-1:5507393815461872:instance/i-t4n5t2ro5em52kfn4mha","timestamp":1726140353000}', 'alertCount': '0', 'nextEscalateTime': '0', 'startTime': '1726140353000', 'time': '1726140353000', 'autoResolveTime': '0'}

url = 'https://aliwebhook.22889.club/aliyun/webhook/37aba484c6261fe79d9729d93a7084c4/Wallet/-4245759043/-4245759043/+KhBOVqnJjswzOTE0'
requests.post(url,data=a)