# from __future__ import annotations
import hashlib
import random
import time

import requests
from fake_useragent import UserAgent
from loguru import logger

import push
from config import Config


class Tieba:
    def __init__(self, tId: str, config: Config):
        self.tId = tId
        self.config = config
        self.account = self._get_account_by_id()
        self.session = requests.session()
        self.headers = {
            'Host': 'tieba.baidu.com',
            'User-Agent': UserAgent().chrome,
            'Connection': 'keep-alive',
            'Cookie': f'BDUSS={self.account.BDUSS}',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        self.check_in_list = []
        self.checked_in_list = []
        self.tbs = self._get_tbs()

    def _get_account_by_id(self):
        for account in self.config.tie_ba_cookie_list.accounts:
            if account.tId == self.tId:
                return account
        logger.info(f"用户{self.tId}不存在")
        logger.error("加载cookie配置文件错误")
        exit(-1)

    @logger.catch
    def _get_tbs(self):
        # 获取用户的tbs
        # 签到的时候需要用到这个参数
        TBS_URL = "http://tieba.baidu.com/dc/common/tbs"
        tbs_rsp = self.session.get(url=TBS_URL, headers=self.headers)
        logger.debug(f'获取用户的tbs响应：{tbs_rsp.text}')
        content = tbs_rsp.json()
        if content['is_login'] == 1:
            logger.success('成功获取用户的tbs')
            return content['tbs']
        else:
            logger.error('获取tbs失败，用户未登录成功。')
            exit(-1)

    @logger.catch
    # 获取用户所关注的贴吧列表
    def get_follows(self):
        # 获取用户所有关注贴吧
        LIKE_URL = "https://tieba.baidu.com/mo/q/newmoindex"
        follow_rsp = self.session.get(url=LIKE_URL, headers=self.headers)
        logger.debug(f'获取用户所关注的贴吧列表响应:{follow_rsp.text}')
        content = follow_rsp.json()
        if content['error'] == 'success':
            logger.success('成功获取用户所关注的贴吧列表')
            for item in content['data']['like_forum']:
                if item['is_sign'] == 0:
                    self.check_in_list.append(item)
                else:
                    self.checked_in_list.append(item)

            logger.debug(f'未签到列表：{self.check_in_list}')
            logger.info(f'签到列表：{self.checked_in_list}')

    @logger.catch
    def check_in(self):
        self.get_follows()
        # 贴吧签到接口
        SIGN_URL = "http://c.tieba.baidu.com/c/c/forum/sign"
        num = 0
        for item in self.check_in_list:
            logger.info(f"开始签到{item['forum_name']}")
            SIGN_DATA = {
                '_client_type': '2',
                '_client_version': '9.7.8.0',
                '_phone_imei': '000000000000000',
                'model': 'MI+5',
                "net_type": "1",
                'BDUSS': self.account.BDUSS,
                'fid': item['forum_id'],
                'kw': item['forum_name'],
                'tbs': self.tbs,
                'timestamp': str(int(time.time()))
            }
            data = self.encodeByMd5(SIGN_DATA)
            check_in_rsp = self.session.post(url=SIGN_URL, headers=self.headers, data=data)
            logger.debug(f"执行{item['forum_name']}签到，响应：{check_in_rsp.text}")
            content = check_in_rsp.json()
            if content['error_code'] == '0':
                logger.success(f"执行{item['forum_name']}签到成功")
                num = + 1
            else:
                logger.warning(f"执行{item['forum_name']}签到失败，失败消息：{content}")

            time.sleep(random.randint(1, 5))
        return self.notice(num)

    @staticmethod
    def encodeByMd5(data):
        s = ""
        keys = data.keys()

        # 遍历键，并根据键进行排序
        for i in sorted(keys):
            s += i + "=" + str(data[i])
        logger.debug(f'未加密数据：{s}')
        # 将排序后的字符串和 SIGN_KEY 进行拼接，然后进行 MD5 加密
        sign = hashlib.md5((s + 'tiebaclient!!!').encode('utf-8')).hexdigest().upper()
        # 将加密结果添加到原始字典中，键为 SIGN，值为加密结果
        data.update({'sign': str(sign)})
        logger.debug(f'加密后的数据：{data}')
        return data

    @logger.catch
    def notice(self, num):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        count = len(self.checked_in_list) + len(self.check_in_list)
        info = f'\n-------------贴吧签到任务情况-------------\n{now}\n共关注{count}个吧~\n' \
               f'今日还剩{len(self.check_in_list)}个吧未签到~\n通过自动任务成功签到{num}个吧~\n还剩{len(self.check_in_list) - num}个吧未签到~'

        if self.account.PUSH_STATUS:
            push.pushplus(self.account.PUSHPLUS_TOKEN, title='贴吧自动签到通知', content=info)
        logger.info(info)
        return info
