# -*- coding: utf-8 -*-
#原始需求：阿里云的视频点播媒体资料库中批量获取到源文件地址来进行下载，脚本只需要提取到所有地址即可
#author:xili
import os
import sys
import json
from typing import List
from alibabacloud_vod20170321.client import Client as vod20170321Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_vod20170321 import models as vod_20170321_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_console.client import Client as ConsoleClient
from alibabacloud_tea_util.client import Client as UtilClient
from Tea.core import TeaCore


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> vod20170321Client:
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/vod
        config.endpoint = f'vod.cn-shanghai.aliyuncs.com'
        return vod20170321Client(config)

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        # 请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID 和 ALIBABA_CLOUD_ACCESS_KEY_SECRET。
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html
        client = Sample.create_client('','')
        get_video_list_request = vod_20170321_models.GetVideoListRequest()
        get_video_list_response = client.get_video_list(get_video_list_request)
        full_size=(json.loads(UtilClient.to_jsonstring(TeaCore.to_map(get_video_list_response)))["body"]["Total"])
        i=1
        try:
            while i-1<full_size:
                get_video_list_request = vod_20170321_models.GetVideoListRequest(page_size=1, page_no=i)
                for video in get_video_list_response.body.video_list.video:
                    get_mezzanine_info_request = vod_20170321_models.GetMezzanineInfoRequest(
                        video_id=video.video_id
                    )
                    get_mezzanine_info_response = client.get_mezzanine_info(get_mezzanine_info_request)
                    zdata = UtilClient.to_jsonstring(TeaCore.to_map(get_mezzanine_info_response))
                    zdata1 = json.loads(zdata)
                    z_file_url = zdata1["body"]["Mezzanine"]["FileURL"]
                    print(z_file_url)
                    i=i+1
        except Exception as error:
            ConsoleClient.log(error.message)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
