import json
import random
import re
from hashlib import md5
from string import digits, ascii_lowercase, ascii_uppercase
from time import time, sleep

import requests
from fake_useragent import UserAgent
from loguru import logger
from requests import Session

import push


class IQY:
    def __init__(self, yId, config):
        self.config = config
        self.yId = yId
        self.account = self._get_account_cookie_by_uId()
        self.iqy_cookie = self.account.iqy_login_cookie
        self.task_list = []
        self.growthTask = 0
        self.sign_in_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Host': 'tc.vip.iqiyi.com',
            'Proxy-Connection': 'keep-alive',
            'Sec-Ch-Ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Cookie': self.iqy_cookie
        }
        self.user_agent = UserAgent().chrome

        try:
            self.P00001 = re.search(r"P00001=(.*?);", self.iqy_cookie).group(1)
            self.dfp = re.search(r'__dfp=(.*?)@', self.iqy_cookie).group(1)
        except Exception as e:
            logger.error(e)
        self.session = Session()
        self.headers = {
            "User-Agent": self.user_agent,
            "Cookie": f"P00001={self.P00001}",
            "Content-Type": "application/json"
        }
        self.uid = ''
        self.qyid = self.md5(self.uuid(16))

    def get_account_cookie_by_uId(self):
        for account in self.config.login_cookie_list.accounts:
            if account.uId == self.yId:
                return account
        logger.info(f"用户{self.yId}不存在")
        logger.error("加载cookie配置文件错误")
        exit(-1)

    def req(self, url, req_method="GET", body=None):
        data = {}
        if req_method.upper() == "GET":
            try:
                data = self.session.get(url, headers=self.headers, params=body).json()
            except Exception as e:
                logger.error("请求发送失败,可能为网络异常")
                logger.error(e)
            #     data = self.session.get(url, headers=self.headers, params=body).text
            return data
        elif req_method.upper() == "POST":
            try:
                data = self.session.post(url, headers=self.headers, data=json.dumps(body)).json()
            except Exception as e:
                logger.error("请求发送失败,可能为网络异常")
                logger.error(e)
            #     data = self.session.post(url, headers=self.headers, data=dumps(body)).text
            return data
        elif req_method.upper() == "OTHER":
            try:
                self.session.get(url, headers=self.headers, params=json.dumps(body))
            except Exception as e:
                logger.error("请求发送失败,可能为网络异常")
                logger.error(e)
        else:
            logger.error("您当前使用的请求方式有误,请检查")

    def getUid(self):
        url = f'https://passport.iqiyi.com/apis/user/info.action?authcookie={self.P00001}&fields=userinfo%2Cqiyi_vip&timeout=15000'
        data = self.req(url)
        logger.debug(f'getUid响应:{data}')
        if data.get("code") == 'A00000':
            self.uid = data['data']['userinfo']['pru']
        else:
            info = f"请求api失败 最大可能是cookie失效了 也可能是网络问题:getUid响应:{data}"
            logger.error(info)
            if self.account.PUSH_STATUS:
                push.pushplus(self.config.push.PUSHPLUS_TOKEN, content="爱奇艺每日任务:" + info)
            exit(-1)

    @staticmethod
    def timestamp(short=False):
        if short:
            return int(time())
        return int(time() * 1000)

    @staticmethod
    def uuid(num, upper=False):
        uuid = ''
        if upper:
            for i in range(num):
                uuid += random.choice(digits + ascii_lowercase + ascii_uppercase)
        else:
            for i in range(num):
                uuid += random.choice(digits + ascii_lowercase)
        return uuid

    @staticmethod
    def md5(uuid):
        m = md5(uuid.encode(encoding='utf-8'))
        return m.hexdigest()

    def get_check_in_url(self):
        time_stamp = self.timestamp()
        self.getUid()
        if self.uid == "":
            logger.error("获取用户id失败 可能为cookie设置错误或者网络异常,请重试或者检查cookie")
            exit(0)
        data = f'agentType=1|agentversion=1|appKey=basic_pcw|authCookie={self.P00001}|qyid={self.qyid}|task_code=natural_month_sign|timestamp={time_stamp}|typeCode=point|userId={self.uid}|UKobMjDMsDoScuWOfp6F'
        url = f'https://community.iqiyi.com/openApi/task/execute?agentType=1&agentversion=1&appKey=basic_pcw&authCookie={self.P00001}&qyid={self.qyid}&sign={self.md5(data)}&task_code=natural_month_sign&timestamp={time_stamp}&typeCode=point&userId={self.uid}'
        return url

    def check_in(self):
        url = self.get_check_in_url()
        body = {
            "natural_month_sign": {
                "taskCode": "iQIYI_mofhr",
                "agentType": 1,
                "agentversion": 1,
                "authCookie": self.P00001,
                "qyid": self.qyid,
                "verticalCode": "iQIYI"
            }
        }
        info = 'null'
        data = self.req(url, "post", body)
        logger.debug(f'签到返回信息：{data}')
        if data.get('code') == 'A00000':
            try:
                msg = data['data']['msg']
                logger.debug(f"msg类型：{type(msg)}")
                # msg为None表示成功执行
                if msg:
                    info = f"签到执行成功, {msg}"
                else:
                    signDays = data['data']['data']['signDays']
                    rewardCount = data['data']['data']['rewards'][0]['rewardCount']
                    info = f"签到执行成功, +{rewardCount}签到成长值,已连续签到{signDays}天。"
                logger.success(info)
            except Exception as e:
                logger.error(e)
            if self.account.PUSH_STATUS:
                push.pushplus(self.account.PUSHPLUS_TOKEN, title="爱奇艺签到通知", content=info)
        else:
            logger.error("签到失败，原因可能是签到接口又又又又改了")

    def _get_account_cookie_by_uId(self):
        for account in self.config.iqy_login_cookie_list.accounts:
            if account.yId == self.yId:
                return account
        logger.info(f"用户{self.yId}不存在")
        logger.error("加载cookie配置文件错误")
        exit(-1)

    def get_user_info(self):
        user_info_url = "http://serv.vip.iqiyi.com/vipgrowth/query.action"
        params = {
            "P00001": self.P00001,
        }
        # user_info_headers = {
        #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        #     'Accept-Encoding': 'gzip,deflate',
        #     'Accept-Language': 'zh-CN,zh;q=0.9',
        #     'Cache-Control': 'max-age=0',
        #     'Host': 'serv.vip.iqiyi.com',
        #     'Proxy-Connection': 'keep-alive',
        #     'Upgrade-Insecure-Requests': '1',
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        #     'Cookie': self.iqy_cookie
        # }
        user_info_resp = requests.get(url=user_info_url, params=params)
        msg = ''
        resp_json = user_info_resp.json()
        if resp_json["code"] == "A00000":
            try:
                res_data = resp_json["data"]
                # VIP等级
                level = res_data["level"]
                # 当前VIP成长值
                growthvalue = res_data["growthvalue"]
                # 升级需要成长值
                distance = res_data["distance"]
                # VIP到期时间
                deadline = res_data["deadline"]
                # 今日成长值
                todayGrowthValue = res_data["todayGrowthValue"]
                msg = f"\n==========爱奇艺会员信息==========\nVIP等级：{level}\n当前成长值：{growthvalue}\n升级需成长值：{distance}\n今日成长值:  +{todayGrowthValue}\nVIP到期时间:{deadline}"
                logger.success("爱奇艺获取会员信息成功")
            except Exception as e:
                logger.warning(resp_json)
                logger.error(e)
        else:
            msg = '爱奇艺获取会员信息失败：' + str(resp_json)
            logger.error(msg)
        logger.info(msg)
        if self.account.PUSH_STATUS:
            push.pushplus(self.account.PUSHPLUS_TOKEN, title='爱奇艺会员信息通知', content=msg)
        return msg

    def sign_in(self):
        sign_url = "https://tc.vip.iqiyi.com/taskCenter/task/queryUserTask"
        params = {
            "P00001": self.P00001,
            "autoSign": "yes"
        }
        check_in_resp = requests.get(url=sign_url, params=params)
        resp_json = check_in_resp.json()
        logger.debug(f'登录成功，响应的数据：{resp_json}')
        if resp_json["code"] == "A00000":
            logger.success("登录任务中心成功")
            return resp_json
        else:
            logger.warning("登录任务中心失败")
            msg = resp_json["msg"]
            return msg

    def query_tasks(self):
        resp_json = self.sign_in()
        if resp_json["code"] == "A00000":
            for item in resp_json["data"]["tasks"]["daily"]:
                self.task_list.append({
                    "name": item["name"],
                    "taskCode": item["taskCode"],
                    "status": item["status"],
                    "taskReward": item["taskReward"]["task_reward_growth"]
                })
        else:
            logger.warning("查询任务状态失败：" + resp_json["msg"])
        logger.success(f"查询任务成功：{self.task_list}")
        return self

    def join_task(self):
        # 遍历完成任务
        join_task_url = "https://tc.vip.iqiyi.com/taskCenter/task/joinTask"
        params = {
            "P00001": self.P00001,
            "taskCode": "",
            "platform": "bb136ff4276771f3",
            "lang": "zh_CN",
            "app_lm": "cn"
        }
        self.query_tasks()
        logger.info(f"任务列表：{self.task_list}")
        # 遍历任务，仅做一次
        for item in self.task_list:
            params["taskCode"] = item["taskCode"]
            logger.info(f"正在执行{item['name']}...")
            res = self.req(url=join_task_url, body=params)
            if res['code'] == 'A00000':
                logger.info(f"加入任务{item['name']}响应:{res}")
                sleep(11)
                logger.info(f"加入任务{item['name']}状态：{res}")
            else:
                logger.error(f"加入任务{item['name']}响应:{res}")

            # 完成任务
            url = f'https://tc.vip.iqiyi.com/taskCenter/task/notify?taskCode={item["taskCode"]}&P00001={self.P00001}&platform=97ae2982356f69d8&lang=cn&bizSource=component_browse_timing_tasks&_={self.timestamp()}'
            if res := self.req(url)['code'] == 'A00000':
                sleep(2)
                logger.info(f"完成任务{item['name']}响应：{res}")

    def get_rewards(self):
        # 获取任务奖励
        rewards_url = "https://tc.vip.iqiyi.com/taskCenter/task/getTaskRewards"
        params = {
            "P00001": self.P00001,
            "taskCode": "",
            "platform": "bb136ff4276771f3",
            "lang": "zh_CN"
        }
        self.join_task()
        logger.info(f'可完成的任务：{self.task_list}')
        # 遍历任务，领取奖励
        for item in self.task_list:
            params["taskCode"] = item["taskCode"]
            res = self.req(url=rewards_url, body=params)
            sleep(1)
            logger.info(f"领取任务{item['name']}状态:{res}")
            if res["code"] == "A00000":
                try:
                    self.growthTask += int(res['data'][0]['成长值'][1])
                except Exception as e:
                    logger.warning(e)
                    pass
        msg = f"+{self.growthTask}任务成长值"
        logger.info(msg)
        if self.account.PUSH_STATUS:
            push.pushplus(self.account.PUSHPLUS_TOKEN, title='爱奇艺领取通知', content=msg)
        return msg
