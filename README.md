#本人已经毕业，项目停止更新
# 目前只有WoZaiXiaoYuan.py这个可以正常打卡，个人使用还是没问题的，多人的懒得改了，可以云函数，可以本地运行
(代码编写不专业，能用就行)
# 如何配置这个程序
下载main.py这个文件，里面我已经注释好了，只需要修改账号密码就行了
# 如何配置微信提醒
打开http://www.pushplus.plus/ 这个网页，使用微信扫码登录，然后点击一对一推送，里面有个token<br>复制token放到文件中的main.py -> pushtoken中就行了(记得关注公众号，不然收不到签到消息)
# 打卡地址
打卡地址默认没填写，需要自己改下sign_data的内容
# 程序依赖
程序运行依赖requests库，你可以使用pip install requests 来安装它

# 如何每天自动运行程序
可以使用定时任务<br>
如何添加定时任务
Linux <a href='https://www.runoob.com/w3cnote/linux-crontab-tasks.html'>点击这里</a>
Windows <a href='https://www.cnblogs.com/gcgc/p/11594467.html'>点击这里</a>

<h2>推荐使用云函数来进行部署</h2><br>

1.首先登录腾讯云控制台https://console.cloud.tencent.com/ 未实名认证的用户需要实名认证后才能使用<br>
2.然后从左上角的云产品中找到云函数![image](https://i1.atlascloud.cn/2021/07/28/b21a90728054853.png)<br>
3.然后点击函数服务，点击新建![image](https://i1.atlascloud.cn/2021/07/28/df4ba0728054935.png)<br>
4.选择自定义创建，运行环境选择python3.6![image](https://i1.atlascloud.cn/2021/07/28/cdf260728055021.png)<br>
5.执行方法输入index.main,然后直接将python代码复制到右边的编辑器中![image](https://i1.atlascloud.cn/2021/07/28/4bc6f0728054614.png)<br>
6.然后点击触发器配置，选择自定义触发周期，输入0 1 0 * * * *，也可以自己设置时间，这里表示每日凌晨12时1分触发![image](https://i1.atlascloud.cn/2021/07/28/2c6fa0728055430.png)<br>
7.点击完成，如果不出意外，应该不需要再手动打卡了，教程结束
