import re

import requests
from loguru import logger

import push


class IQY:
    def __init__(self, yId, config):
        self.config = config
        self.yId = yId
        self.iqy_cookie = self._get_account_cookie_by_uId().iqy_login_cookie
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
        self.P00001 = re.findall(r"P00001=(.*?);", self.iqy_cookie)

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
        user_info_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip,deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Host': 'serv.vip.iqiyi.com',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'Cookie': self.iqy_cookie
        }
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
        if self.config.push.PUSH_OR_NOR:
            push.pushplus(self.config.push.PUSHPLUS_TOKEN, title='爱奇艺会员信息通知', content=msg)
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
            "lang": "zh_CN"
        }
        self.query_tasks()
        logger.info(f"任务列表：{self.task_list}")
        # 遍历任务，仅做一次
        for item in self.task_list:
            if item["status"] == 2:
                params["taskCode"] = item["taskCode"]
                res = requests.get(url=join_task_url, params=params)
                logger.info(f"加入任务{item['name']}状态：{res.text}")
            else:
                logger.success(f"日常任务{item['name']}加入成功...")
            # time.sleep(3)

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
        logger.debug(f'可完成的任务：{self.task_list}')
        # 遍历任务，领取奖励
        for item in self.task_list:
            if item["status"] == 0:
                params["taskCode"] = item["taskCode"]
                res = requests.get(url=rewards_url, params=params)
                logger.debug(res.text)
                if res.json()["code"] == "A00000":
                    self.growthTask += item["taskReward"]
        msg = f"+{self.growthTask}成长值"
        logger.info(msg)
        # if self.config.push.PUSH_OR_NOR:
        #     push.pushplus(self.config.push.PUSHPLUS_TOKEN,title='爱奇艺领取通知',content=msg)
        return msg
