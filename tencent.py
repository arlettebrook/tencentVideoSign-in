# -*- coding: utf8 -*-
import json
import time

import requests
from loguru import logger

import config
import data
import push


def tencent_video_login():
    millisecond_time = round(time.time() * 1000)
    login_headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '644',
        'Content-Type': 'application/json',
        'Origin': 'https://v.qq.com',
        'Referer': 'https://v.qq.com/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Cookie': config.login_cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    try:
        body = json.dumps(config.login_url_payload)
        login_rsp = requests.post(url=config.login_url, data=body, headers=login_headers)
        if login_rsp.status_code == 200:
            logger.info("登录成功")
            logger.debug("登录数据：" + login_rsp.text)
            logger.debug(f"获取到的cookies：{login_rsp.cookies}", )
            return login_rsp
        else:
            logger.error("登录失败：" + login_rsp.text)
    except Exception as e:
        logger.exception("可能是请求出错")


def get_cookies():
    login_rsp = tencent_video_login()
    cookies = login_rsp.cookies
    vqq_vusession = cookies.get('vqq_vusession')
    vqq_access_token = cookies.get('vqq_access_token')
    vqq_appid = cookies.get('vqq_appid')
    vqq_openid = cookies.get('vqq_openid')
    vqq_refresh_token = cookies.get('vqq_refresh_token')
    vqq_vuserid = cookies.get('vqq_vuserid')
    vqq_next_refresh_time = cookies.get('vqq_next_refresh_time')
    vqq_login_time_init = cookies.get('vqq_login_time_init')

    auth_cookie = config.auth_cookie + vqq_vusession + ';' + 'vqq_access_token=' + \
                  vqq_access_token + ';' + 'vqq_appid=' + vqq_appid + ';' + 'vqq_openid=' + vqq_openid + ';' + 'vqq_refresh_token=' + \
                  vqq_refresh_token + ';' + 'vqq_vuserid=' + vqq_vuserid + ';' + 'vqq_next_refresh_time=' + vqq_next_refresh_time + ';' + 'vqq_login_time_init=' + vqq_login_time_init
    logger.info('auth_cookie:' + auth_cookie)
    return auth_cookie


def tencent_video_auto_sign():
    auth_cookie = get_cookies()
    sign_in_url = "https://vip.video.qq.com/rpc/trpc.new_task_system.task_system.TaskSystem/CheckIn?rpc_data={}"
    referer = 'https://film.video.qq.com/x/grade/?ovscroll=0&ptag=Vgrade.card&source=page_id=default&ztid=default&pgid=page_personal_center&page_type=personal&is_interactive_flag=1&pg_clck_flag=1&styletype=201&mod_id=sp_mycntr_vip&sectiontype=2&business=hollywood&layouttype=1000&section_idx=0&mod_title=会员资产&blocktype=6001&vip_id=userCenter_viplevel_entry&mod_idx=11&item_idx=4&eid=button_mycntr&action_pos=jump&hidetitlebar=1&isFromJump=1&isDarkMode=1&uiType=HUGE'
    referer = referer.encode("utf-8").decode("latin1")
    sign_headers = {
        'Referer': referer,
        'Host': 'vip.video.qq.com',
        'Origin': 'https://film.video.qq.com',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 11; PCAM00 Build/RKQ1.201217.002)',
        'Accept-Encoding': 'gzip, deflate, br',
        "Cookie": auth_cookie
    }
    sign_rsp = requests.get(url=sign_in_url, headers=sign_headers)

    logger.debug("签到响应内容：" + sign_rsp.text)

    sign_rsp_json = sign_rsp.json()

    if sign_rsp_json['ret'] == 0:
        score = sign_rsp_json['checkin_score']
        if score == '0':
            log = f'Cookie有效!当天已签到'
        else:
            log = f'Cookie有效!签到成功,获得经验值{score}'
    elif sign_rsp_json['ret'] == -2002:
        log = f'Cookie有效!当天已签到'
    else:
        log = sign_rsp_json['msg']
        logger.error(log)
    logger.debug('签到状态：' + log)

    # requests.get('https://sc.ftqq.com/自己的sever酱号.send?text=' + quote('签到积分：' + str(rsp_score)))

    # logger.info(f'已添加{len(config.COOKIE_LIST)}个cookie')
    # for x in config.COOKIE_LIST:
    #     sign_headers = {
    #         'cookie': x
    #     }
    #     res = requests.get(url=sign_url, headers=sign_headers).text
    #     res_json_list = re.findall(data.json_pattern, res)
    #     res_json = json.loads(res_json_list[0])
    #     logger.info(res_json)

    if config.PUSH_OR_NOR:
        push.pushplus(log, config.PUSHPLUS_TOKEN)
    return log


def tencent_video_get_vip_info():
    auth_cookies = get_cookies()
    vip_info_headers  = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Length': '46',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Origin': 'https://film.qq.com',
        'Referer': 'https://film.qq.com/vip/my/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Cookie': auth_cookies,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    body = json.dumps(config.get_vip_info_url_payload)
    vip_info_rsp = requests.post(data.get_vip_info_url, data=body, headers=vip_info_headers)
    if vip_info_rsp.status_code == 200:
        logger.debug("获取会员信息状态："+vip_info_rsp.text)
        # handle_vip_info(vip_info_rsp.json())
        return vip_info_rsp.json()
    else:
        logger.error("获取会员信息响应失败")
