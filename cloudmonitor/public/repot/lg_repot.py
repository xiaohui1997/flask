import sys
sys.path.append("/data/flask")

import requests
from Public.config import FEISHU_CONFIG_LG_REPORT as FEISHU_CONFIG
import requests
from Public.lark import get_signed_params


from Public.c_moni import get_cms_client, get_metric_data, get_timestamps

# 创建客户端(云监控只读权限，权限可控。)
access_key_id = "LTAI5tCRpJVfk8aUt3uC37iz"
access_key_secret = "hJgmdS1RcDRTr7ZMRZ4Ryqs9wjuQqF"
cms_client = get_cms_client(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret
)


# 渲染表格的函数
def render_table(data, title="内存使用率"):
    # 找出实例名称的最大长度，确保列宽一致
    max_name_length = max(len(item[0]) for item in data)
    
    # 表格头
    result = f"----{title}------\n"
    
    # 遍历数据生成每一行
    for item in data:
        instance_name, value = item
        # 动态调整列宽，{max_name_length} 确保名称列宽度一致
        result += f"| {instance_name:<{max_name_length + 2 }} | {value:.2f}  |\n"
    
    return result

def get_ecs_data():
    #ecs 监控数据
    # 实例信息
    namespace = 'acs_ecs_dashboard'
    # 实例名称映射
    instance_name_mapping = {
        'i-5tse5mv21pbb5o3k6f30': 'lg-prod-nginx',
        'i-5ts3xe4ep8yn0zpcnynx': 'lg-prod-operations',
        'i-5tse5mv21pbb5m4j2d3v': 'lg-prod-app',
        'i-5ts3xe4ep8yn0vrafupo': 'lg-prod-sabong-ws',
        'i-5ts8lvyyprw34rdh9gva': 'lg-prod-crash-ws',
        'i-5ts48r88mlgeuhpvesma': 'lg-prod-xxljob',
    }
    #指标列表
    metric_name_list = {
        'CPUUtilization': 'CPU使用率',
        'memory_usedutilization': '内存使用率',
        'diskusage_utilization': '磁盘使用率'
    }
    msg = '''
【服务器指标✅】

| 实例名称| 指标值 |
'''
    for metric_name, metric_name_cn in metric_name_list.items():
        #指标排序
        metric_sort = []
        for instance_id, instance_name in instance_name_mapping.items():
            # 获取时间戳
            start_time, end_time = get_timestamps(hours=1)

            # 获取监控数据
            result = get_metric_data(
                client=cms_client,
                namespace=namespace,
                metric_name=metric_name,
                instance_id=instance_id,
                start_time=end_time,
                end_time=start_time
            )

            res = eval(result.datapoints)
            metric_sort.append([instance_name, res[-1]['Average']]) #ecs 最新一条数据 取Average
        sorted_data = sorted(metric_sort, key=lambda x: x[1], reverse=True)

        # 调用函数生成表格
        table = render_table(sorted_data,metric_name_cn)

        # 打印结果
        msg += table
    return msg

def get_rds_data():
    #rds 监控数据
    namespace = 'acs_rds_dashboard'
    instance_name_mapping = {
        'rm-5ts57ww391t919389': 'lg-prod-mysql'
    }
    #指标列表
    metric_name_list = {
        'CpuUsage': 'CPU使用率',
        'MemoryUsage': '内存使用率',
        'DiskUsage': '磁盘使用率',
        'ConnectionUsage': '连接数使用率'
    }
    msg = '''
【RDS指标✅】

| 实例名称| 指标值 |
'''
    for metric_name, metric_name_cn in metric_name_list.items():
        #指标排序
        metric_sort = []
        for instance_id, instance_name in instance_name_mapping.items():
            # 获取时间戳
            start_time, end_time = get_timestamps(hours=1)

            # 获取监控数据
            result = get_metric_data(
                client=cms_client,
                namespace=namespace,
                metric_name=metric_name,
                instance_id=instance_id,
                start_time=end_time,
                end_time=start_time
            )

            res = eval(result.datapoints)
            metric_sort.append([instance_name, res[-1]['Average']])
        sorted_data = sorted(metric_sort, key=lambda x: x[1], reverse=True)

        # 调用函数生成表格
        table = render_table(sorted_data,metric_name_cn)

        # 打印结果
        msg += table
    return msg


def get_kafka_data():
    #kafka 监控数据
    namespace = 'acs_kafka'
    msg = '''
【Kafka指标✅】

| Grop名称| 堆积量 |
'''
    # 实例名称映射
    instance_name_mapping = {
        'alikafka_pre_public_intl-sg-d6a411vht01': 'lg-prod',
    }
    #指标列表
    metric_name_list = {
        'message_accumulation': '消息堆积量'
    }
    for metric_name, metric_name_cn in metric_name_list.items():
        #指标排序
        metric_sort = []
        for instance_id, instance_name in instance_name_mapping.items():
            # 获取时间戳
            start_time, end_time = get_timestamps(hours=1)

            # 获取监控数据
            result = get_metric_data(
                client=cms_client,
                namespace=namespace,
                metric_name=metric_name,
                instance_id=instance_id,
                start_time=end_time,
                end_time=start_time
            )

            res = eval(result.datapoints)
            metric_sort.append([res[-1]['consumerGroup'], res[-1]['Value']])
            metric_sort.append([res[-2]['consumerGroup'], res[-2]['Value']])
            metric_sort.append([res[-3]['consumerGroup'], res[-3]['Value']])
            metric_sort.append([res[-4]['consumerGroup'], res[-4]['Value']])
            metric_sort.append([res[-5]['consumerGroup'], res[-5]['Value']])
        sorted_data = sorted(metric_sort, key=lambda x: x[1], reverse=True)

        # 调用函数生成表格
        table = render_table(sorted_data,metric_name_cn)
        # 打印结果
        msg += table
    return msg

def get_redis_data():
    #redis 监控数据
    namespace = 'acs_kvstore'
    instance_name_mapping = {
        'r-5tsmoe5bozu7p9eerz': 'lg-prod-redis'
    }
    #指标列表
    metric_name_list = {
        'StandardCpuUsage': 'CPU使用率',
        'StandardMemoryUsage': '内存使用率'
    }
    msg = '''
【Redis指标✅】

| 实例名称| 指标值 |
'''
    for metric_name, metric_name_cn in metric_name_list.items():
        #指标排序
        metric_sort = []
        for instance_id, instance_name in instance_name_mapping.items():
            # 获取时间戳
            start_time, end_time = get_timestamps(hours=1)

            # 获取监控数据
            result = get_metric_data(
                client=cms_client,
                namespace=namespace,
                metric_name=metric_name,
                instance_id=instance_id,
                start_time=end_time,
                end_time=start_time
            )

            res = eval(result.datapoints)
            metric_sort.append([instance_name, res[-1]['Average']])
        sorted_data = sorted(metric_sort, key=lambda x: x[1], reverse=True)

        # 调用函数生成表格
        table = render_table(sorted_data,metric_name_cn)

        # 打印结果
        msg += table
    return msg

msg = get_ecs_data() #ecs 监控数据
msg += get_rds_data() #rds 监控数据
msg += get_kafka_data() #kafka 监控数据
msg += get_redis_data() #redis 监控数据

print('#'*30)
print(msg)


def send_message_recover():
    """
    ecs告警
    """
    
    # 获取签名参数
    data = get_signed_params(FEISHU_CONFIG["secret"])

    data.update({
        "msg_type": "post",
    "content": {
        "post": {
            "zh_cn": {
                "title": "1小时指标报告",
                "content": [
                    [
                        {
                            "tag": "text",
                            "text": msg
                        }
                    ]
                ]
            }
        }
    }
    })
            
    headers = {"Content-Type": "application/json"}
    response = requests.post(FEISHU_CONFIG["webhook_url"], headers=headers, json=data)
    return response

send_message_recover()