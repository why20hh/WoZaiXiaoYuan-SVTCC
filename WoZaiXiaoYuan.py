import requests
import json
from urllib.parse import urlencode
import time
import hashlib

class Start:
    def __init__(self):
        self.pushtoken = ''  # 这里填pushplus的token，可以在http://www.pushplus.plus/ 扫码注册
        self.jwsession = ''  # 这里填我在校园的jwsession
        self.sign_time = int(round(time.time() * 1000))  # 13位
        self.dk = {
            'token': self.pushtoken,
            'title': '我在校园每日打卡',
            'content': '',
        }
        self.header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": "2",
            "Host": "student.wozaixiaoyuan.com",
            "Accept-Language": "en-us,en",
            "Accept": "application/json, text/plain, */*",
            'JWSESSION':self.jwsession
        }
        self.dkurl = 'http://www.pushplus.plus/send'
        self.body = "{}"

    def get_end(self):
        url = "https://student.wozaixiaoyuan.com/health/save.json"
        sign_data = {
            "answers": '["0"]',
            "latitude": "",  # 纬度
            "longitude": "",  # 经度
            "country": "",  # 国家
            "city": "",  # 城市
            "district": "",  # 区、县
            "province": "",  # 省
            "township": "",  # 可以不填
            "street": "",  # 可以不填
        }
        content = f"四川省_{self.sign_time}_成都市"
        signature = hashlib.sha256(content.encode('utf-8')).hexdigest()
        sign_data["timestampHeader"] = self.sign_time
        sign_data["signatureHeader"] = signature
        print(sign_data)
        data = urlencode(sign_data)
        response = requests.post(url=url, data=data, headers=self.header)
        response = json.loads(response.text)
        print(response)
        if response["code"] == 0:
            self.dk['content'] = "打卡成功"
            re = requests.post(url=self.dkurl, data=self.dk)
            print(re.text)
        else:
            self.dk['content'] = "打卡失败"
            re = requests.post(url=self.dkurl, data=self.dk)
            print(re.text)

def main(event,context):
    dk = Start()
    dk.get_end()

if __name__ == '__main__':
    main()
