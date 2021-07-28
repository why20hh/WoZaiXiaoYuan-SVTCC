# 关于这个打卡程序
秉持着能坐着绝不站着,能躺着绝不坐着的原则，发布了这个打卡程序
(代码编写不专业，能用就行)
# 如何配置这个程序
下载main.py这个文件，里面我已经注释好了，只需要修改账号密码就行了

# 如何配置微信提醒
打开http://www.pushplus.plus/ 这个网页，使用微信扫码登录，然后点击一对一推送，里面有个token<br>复制token放到文件中的main.py -> pushtoken中就行了(记得关注公众号，不然收不到签到消息)

# 如何运行这个程序
程序运行依赖requests库，你可以使用pip install requests 来安装它

# 如何每天自动运行程序
可以使用定时任务<br>
如何添加定时任务
Linux <a href='https://www.runoob.com/w3cnote/linux-crontab-tasks.html'>点击这里</a>
Windows <a href='https://www.cnblogs.com/gcgc/p/11594467.html'>点击这里</a>

推荐使用云函数来进行部署
