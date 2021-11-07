# -*- encoding:utf-8 -*-
import requests
import json
from urllib.parse import urlencode
import os
import time
import random
import pytz
import datetime

class Health:
    def __init__(self):
        # JWSESSION
        self.jwsession = None
        # 打卡结果
        self.status_code = 0
        # 登陆接口
        self.loginUrl = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
        # 请求头
        self.header = {
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Content-Type": "application/json;charset=UTF-8",
            "Content-Length": "2",
            "Host": "gw.wozaixiaoyuan.com",
            "Accept-Language": "en-us,en",
            "Accept": "application/json, text/plain, */*"
        }
        # 请求体（必须有）
        self.body = "{}"
        self.user = {
            'username' : user,
            'passwd' : passwd
        }
        self.cache = cache
        self.session = requests.session()

    def login(self):
        username, password = str(self.user['username']), str(self.user['passwd'])
        url = f'{self.loginUrl}?username={username}&password={password}'
        self.session = requests.session()
        # 登录
        response = self.session.post(url=url, data=self.body, headers=self.header)
        res = json.loads(response.text)
        if res["code"] == 0:
            print("使用账号信息登录成功")
            jwsession = response.headers['JWSESSION']
            self.setJwsession(jwsession)
            return True
        else:
            print(res)
            print("登录失败，请检查账号信息")
            self.status_code = 5
            return False

    # 设置JWSESSION
    def setJwsession(self, jwsession):
        # 如果找不到cache,新建cache储存目录与文件
        if not os.path.exists(self.cache):
            print("正在创建cache文件...")
            data = {"jwsession": jwsession}
        # 如果找到cache,读取cache并更新jwsession
        else:
            print("找到cache文件，正在更新cache中的jwsession...")
            f = open(self.cache, encoding='utf-8')
            res = f.read()
            f.close()
            data = json.loads(res)
            with open(self.cache, 'w') as json_file:
                data['jwsession'] = jwsession

        self.jwsession = data['jwsession']
        with open(self.cache, 'w') as json_file:
            json.dump(data, json_file)


        # 获取JWSESSION

    def getJwsession(self):
        if not self.jwsession:  # 读取cache中的配置文件
            f = open(self.cache, encoding='utf-8')
            res = f.read()
            f.close()
            data = json.loads(res)

            self.jwsession = data['jwsession']
        return self.jwsession

    # 随机体温
    def get_random_temprature(self):
        random.seed(time.ctime())
        return "{:.1f}".format(random.uniform(36.1, 36.5))

    def get_seq(self):
        tz = pytz.timezone('Asia/Shanghai')
        current_hour = datetime.datetime.now(tz)
        print("当前时间是:" + current_hour.strftime("%Y-%m-%d %H:%M:%S"))
        current_hour = current_hour.hour
        if 6 <= current_hour <= 9:
            return "1"
        elif 11 < current_hour <= 14:
            return "2"
        elif 17 < current_hour < 21:
            return "3"
        else:
            return 0
    def check(self):
        if self.get_seq() == "1":
            return "晨检"
        elif self.get_seq() == "2":
            return "午检"
        elif self.get_seq() == "3":
            return "晚检"
        else:
            return "未知"

    # 执行打卡
    def doPunchIn(self):
        print("正在打卡...")
        url = "https://student.wozaixiaoyuan.com/heat/save.json"
        self.header['Host'] = "student.wozaixiaoyuan.com"
        self.header['Content-Type'] = "application/x-www-form-urlencoded"
        self.header['JWSESSION'] = self.getJwsession()

        #sign_data = dldata
        sign_data = {
            "answers": '["0"]',
            "seq": self.get_seq(),
            "temperature":self.get_random_temprature(),
            "latitude": "30.68800939192702",
            "longitude": "103.81650371398926",
            "country": "中国",
            "city": "成都市",
            "district": "温江区",
            "province": "四川省",
            "township": "",
            "street": "",
        }
        data = urlencode(sign_data)
        response = self.session.post(url=url, data=data, headers=self.header)
        response = json.loads(response.text)
        # 打卡情况
        # 如果 jwsession 无效，则重新 登录 + 打卡
        if response['code'] == -10:
            print('jwsession 无效，将尝试使用账号信息重新登录')
            self.status_code = 4
            loginStatus = self.login()
            if loginStatus:
                self.doPunchIn()
            else:
                print("重新登录失败，请检查账号信息")
        elif response["code"] == 0:
            self.status_code = 1
            print("打卡成功")
        elif response['code'] == 1:
            self.status_code = 3
            print("打卡失败：今日健康打卡已结束")
        else:
            print(response)
            print("打卡失败")

    # 获取打卡结果
    def getResult(self):
        res = self.status_code
        if res == 1:
            return "✅ 打卡成功"
        elif res == 2:
            return "✅ 你已经打过卡了，无需重复打卡"
        elif res == 3:
            return "❌ 打卡失败，当前不在打卡时间段内"
        elif res == 4:
            return "❌ 打卡失败，jwsession 无效"
        elif res == 5:
            return "❌ 打卡失败，登录错误，请检查账号信息"
        else:
            return "❌ 打卡失败，发生未知错误，请检查日志"

    # 推送打卡结果
    def sendNotification(self):
        url = 'https://ts.xhyun.online/send_private_msg'
        notifyResult = self.getResult()
        dktime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msg = {
            'user_id': qq,
            'message': '⏰ ' + self.check()+ '打卡情况:' +notifyResult + '\n' +'打卡时间:' + dktime,

        }
        re = requests.post(url, params=msg)
        print(re.text)

def main():
    dk = Health()
    if not os.path.exists(cache):
        print("找不到cache文件，正在使用账号信息登录...")
        loginStatus = dk.login()
        if loginStatus:
            dk.doPunchIn()
        else:
            print("登陆失败，请检查账号信息")
    else:
        print("找到cache文件，尝试使用jwsession打卡...")
        dk.doPunchIn()
    # 推送打卡结果
    dk.sendNotification()
    return True

if __name__ == "__main__":
    with open('/dk/shu.json', 'r', encoding='utf8')as fp:
        json_data = json.load(fp)
        for key in json_data:
            user = key['username']
            passwd = key['password']
            cache = key['cache']
            qq = key['qq']
            print('当前打卡用户:' + user)
            main()
            time.sleep(5)
