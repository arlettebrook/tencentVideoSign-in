# -*- coding: utf8 -*-
import re
import json
import requests


import config
import data
import push


def tencent_video_sign():
    sign_url = data.sign_url
    print(f'已添加{len(config.COOKIE_LIST)}个cookie')
    for x in config.COOKIE_LIST:
        sign_headers = {
            'cookie': x
        }
        res = requests.get(url=sign_url, headers=sign_headers).text
        res_json_list = re.findall(data.json_pattern, res)
        res_json = json.loads(res_json_list[0])
        print(res_json)
        if res_json['ret'] == 0:
            score = res_json['checkin_score']
            if score == '0':
                log = f'Cookie有效!当天已签到'
            else:
                log = f'Cookie有效!签到成功,获得经验值{score}'
        elif res_json['ret'] == -2002:
            log = f'Cookie有效!当天已签到'
        else:
            log = 'Cookie失效!'
        print(log)
        if config.PUSH_OR_NOR:
            push.pushplus(config.PUSHPLUS_TOKEN, log)