import requests
import json


def pushplus(content,token,template='markdown'):
    title = '腾讯视频签到提醒'
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template":"markdown"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=body, headers=headers)
    return response