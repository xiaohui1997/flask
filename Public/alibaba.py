# -*- coding: utf-8 -*-

#pip install alibabacloud_sas20181203==3.2.0

from alibabacloud_sas20181203.client import Client as Sas20181203Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sas20181203 import models as sas_20181203_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import requests


class Sample:
    def __init__(self, access_key_id, access_key_secret, region):
        self.access_key_id = access_key_id  # 请使用安全的方式存储密钥
        self.access_key_secret = access_key_secret
        self.region = region

    def create_client(self) -> Sas20181203Client:
        """
        Initialize the Client with the AccessKey of the account
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=self.access_key_id,  # 请使用安全的方式存储密钥
            access_key_secret=self.access_key_secret
        )

        url='https://api.aliyun.com/meta/v1/products/Sas/endpoints.json?language=zh-CN'
        response = requests.get(url).json()
        endpoint = None
        for i in response['data']['endpoints']:
            if i['regionId'] == self.region:
                endpoint = i['public']
        config.endpoint = 'tds.{}.aliyuncs.com'.format(endpoint)
        return Sas20181203Client(config)

    # @staticmethod
    # def main() -> None:
    #     client = Sample.create_client()
    #
    #     # 直接在这里定义请求参数
    #     describe_susp_events_request = sas_20181203_models.DescribeSuspEventsRequest(
    #         uuids='6cabbe22-c6e2-4894-94aa-7b6045623275',
    #         unique_info='535649f363c03cd81412dbcc6d248cf2'
    #     )
    #
    #     runtime = util_models.RuntimeOptions()
    #
    #     try:
    #         # 调用API并处理返回值
    #         response = client.describe_susp_events_with_options(describe_susp_events_request, runtime)
    #         print(response)  # 打印返回的响应内容
    #
    #     except Exception as error:
    #         # 处理异常情况
    #         print("Error:", error.message)
    #         print("Recommendation:", error.data.get("Recommend"))
    #         UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    #res = Sample.main()  # 直接调用main方法，无需命令行参数
    client = Sample.create_client()
    # 直接在这里定义请求参数
    describe_susp_events_request = sas_20181203_models.DescribeSuspEventsRequest(
        uuids='6cabbe22-c6e2-4894-94aa-7b6045623275',
        unique_info='535649f363c03cd81412dbcc6d248cf2'
    )

    runtime = util_models.RuntimeOptions()

    # 调用API并处理返回值
    response = client.describe_susp_events_with_options(describe_susp_events_request, runtime)
    print(response)  # 打印返回的响应内容
