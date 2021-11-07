# -*- encoding:utf-8 -*-
import requests
import json
from urllib.parse import urlencode

pushtoken = ''  # 这里填pushplus的token，可以在http://www.pushplus.plus/ 扫码注册
jwsession = ''  # 这里填我在校园的jwsession

dk = {
    'token': pushtoken,
    'title': '我在校园每日打卡',
    'content': '',
}
header = {
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    "Content-Type": "application/json;charset=UTF-8",
    "Content-Length": "2",
    "Host": "gw.wozaixiaoyuan.com",
    "Accept-Language": "en-us,en",
    "Accept": "application/json, text/plain, */*"
}
dkurl = 'http://www.pushplus.plus/send'
body = "{}"

try:
    def main():
        header['JWSESSION'] = jwsession
        header['Host'] = "student.wozaixiaoyuan.com"
        header['Content-Type'] = "application/x-www-form-urlencoded"
        url = "https://student.wozaixiaoyuan.com/health/save.json"
        sign_data = {
            "answers": '["0"]',
            "latitude": "30.694365",  # 纬度
            "longitude": "103.822602",  # 经度
            "country": "中国",  # 国家
            "city": "成都市",  # 城市
            "district": "温江区",  # 区、县
            "province": "四川省",  # 省
            "township": "",  # 可以不填
            "street": "",  # 可以不填
        }
        data = urlencode(sign_data)
        response = requests.post(url=url, data=data, headers=header)
        response = json.loads(response.text)
        print(response)
        if response["code"] == 0:
            dk['content'] = "打卡成功"
            re = requests.post(url=dkurl, data=dk)
            print(re.text)
        else:
            dk['content'] = "打卡失败"
            re = requests.post(url=dkurl, data=dk)
            print(re.text)

    if __name__ == '__main__':
        main()

except:
    dk['content'] = '运行出错,请检查'
    re = requests.post(url=dkurl, data=dk)
    print(re.text)
