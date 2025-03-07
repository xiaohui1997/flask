# -*- coding: utf-8 -*-
import os
from alibabacloud_cms20190101.client import Client as Cms20190101Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_cms20190101 import models as cms_20190101_models
from alibabacloud_tea_util import models as util_models
from datetime import datetime, timedelta
import pytz


def get_timestamps(hours=1):
    """
    获取当前时间和一小时之前的时间戳
    :param hours: 时间间隔（小时），默认为1小时
    :return: 当前时间和一小时之前的时间戳
    """
    # 定义时区为北京时间/上海时间
    tz = pytz.timezone('Asia/Shanghai')
    
    # 获取当前时间
    now = datetime.now(tz)
    
    # 获取一小时之前的时间
    one_hour_ago = now - timedelta(hours=hours)
    
    # 转换为时间戳
    #current_timestamp = int(now.timestamp())
    #one_hour_ago_timestamp = int(one_hour_ago.timestamp())
    
    #return current_timestamp, one_hour_ago_timestamp
    return now.strftime('%Y-%m-%d %H:%M:%S'), one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')


def get_cms_client(access_key_id=None, access_key_secret=None, region='ap-southeast-6'):
    """
    获取阿里云CMS客户端
    :param access_key_id: 访问密钥ID
    :param access_key_secret: 访问密钥密码
    :param region: 地区，默认为ap-southeast-6
    :return: CMS客户端实例
    云监控获取监控数据
    """
    # 如果没有提供access key，则尝试从环境变量获取
    if not access_key_id:
        access_key_id = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_ID')
    if not access_key_secret:
        access_key_secret = os.environ.get('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
    
    if not access_key_id or not access_key_secret:
        raise ValueError("AccessKey ID和Secret必须通过参数提供或在环境变量中设置")

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret
    )
    config.endpoint = f'metrics.{region}.aliyuncs.com'
    return Cms20190101Client(config)

def get_metric_data(client, namespace, metric_name, instance_id, start_time, end_time, period='60'):
    """
    获取指定指标的监控数据
    :param client: CMS客户端实例
    :param namespace: 命名空间
    :param metric_name: 指标名称
    :param instance_id: 实例ID
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param period: 时间间隔（秒）
    :return: 监控数据
    """
    request = cms_20190101_models.DescribeMetricListRequest(
        namespace=namespace,
        metric_name=metric_name,
        period=period,
        dimensions=f'[{{"instanceId":"{instance_id}"}}]',
        start_time=start_time,
        end_time=end_time
    )
    runtime = util_models.RuntimeOptions()
    
    try:
        result = client.describe_metric_list_with_options(request, runtime)
        return result.body
    except Exception as error:
        print(f"获取监控数据失败: {error.message}")
        if hasattr(error, 'data') and error.data:
            print(f"建议: {error.data.get('Recommend')}")
        raise
    
# 使用示例
if __name__ == '__main__':
    try:
        # 创建客户端
        cms_client = get_cms_client(
            access_key_id="YOUR_ACCESS_KEY_ID",
            access_key_secret="YOUR_ACCESS_KEY_SECRET"
        )
        
        # 获取监控数据
        result = get_metric_data(
            client=cms_client,
            namespace='acs_ecs_dashboard',
            metric_name='memory_usedutilization',
            instance_id='i-5ts8yx25102zbrrb9p3v',
            start_time='2025-02-28 17:00:00',
            end_time='2025-02-29 00:00:00'
        )
        
        print("监控数据:")
        print(result)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")