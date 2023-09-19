<p align="center">
  <h2 align="center"><storng>腾讯视频登录</storng></h2>
</p>



---



## 🍜使用说明



> 更多方法自己查看源码



### 🥗腾讯视频使用说明



- 配置`config.cfg`配置文件中的  LOGIN_COOKIE 、LOGIN_URL、 LOGIN_URL_PAYLOADLOAD、PUSHPLUS_TOKEN、GET_VIP_INFO_URL_PAYLOAD几个参数，对象调用方法即可使用。
- TencentVideo对象提供三个方法：
  - tencent_video_auto_sign()：自动签到函数
  - tencent_video_get_vip_info()：查询会员信息
    - 这个方法还会领取一小时V力值任务【前提已完成，否则为0】
    - uId为不同用户标识，配置文件中自定义


---



### 🧶爱奇艺使用说明

- 配置`config.cfg`配置文件中的 `iqy_login_cookie`,对象调方法既可以使用。
- IQY对象提供三个方法：
  - get_user_info():获取爱奇艺会员信息
  - get_rewards():领取已完成的每日任务

---



### 🍔贴吧使用说明

- 配置`config.cfg`配置文件中的 `BDUSS`,对象调方法既可以使用。
- TieBa对象提供1个方法：
  - check_in()：签到所有贴吧



---



## 🥯如何抓取COOKIE

### 🙍🏻‍♂️login_cookie等参数的获取

1. 网页登录 [腾讯视频](v.qq.com)
2. 进入该网页：https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2
3. F12 输入在控制台输入document.cookie然后回车，得到的全部信息就是login_cookie；
4. 获取配置信息的效果图如下：
   ![获取配置信息](README.assets/1.jpg)

5. 或者登录成功之后F12，F5依次输入，然后搜索NewRefresh，这个url就是`LOGIN_URL`， `LOGIN_URL_PAYLOADLOAD`就是这个url的请求体。
6. `PUSHPLUS_TOKEN`公众号pushplus获取

> - 注意：
>   - 如果报错没有通过图像验证，需要在cookie中加入vdevice_qimei36='...'[使用常用手机打开获取](https://m.v.qq.com/schemeurl)。
>   - 加上使用一段时间之后，又出现图形验证，需要手动签到一次。

7. `GET_VIP_INFO_URL_PAYLOAD`[同样方法获取该链接的请求体](https://vip.video.qq.com/rpc/trpc.query_vipinfo.vipinfo.QueryVipInfo/GetVipUserInfoH5)
7. 爱奇艺的`IQY_COOKIE`同理，扫码登录[爱奇艺](https://iqyi.com)官网之后，点击[链接](http://serv.vip.iqiyi.com/vipgrowth/query.action)进入控制台查看cookie
7. 网址扫码登录贴吧官网之后，然后按下`F12`打开调试模式，在`cookie`中找到`BDUSS`，并复制其`Value`值。



---



## 📞注意事项

- 推送代码只写了PUSHPLUS的，可以自己拓展其他的推送
- 已经测试COOKIE有效时间超过三个月 目前还没过期
- 腾讯视频
  - 不是所有帐号都能签到成功因为有的帐号会触发滑块认证或者短信验证
  - 使用常用手机打开后面的连接，注意是https，成功进入之后点击查看设备信息，QIMEI36字段就是vdevice_qimei36='...'，按照cookie格式加在LOGIN_COOKIE末尾即可。
  - 注意：如果你平时签到之类的都需要验证码和滑块验证，加上这个字段之后并不能解决问题。目前部分账号会出现安全验证。




---



## ✨相似项目

- [bigoceans/TencentVideoAutoCheck](https://github.com/bigoceans/TencentVideoAutoCheck)

- [bigoceans/TencentVideoAutoCheck2.0](https://github.com/bigoceans/TencentVideoAutoCheck2.0)

- [LuoSue/TiebaSignIn-1](https://github.com/LuoSue/TiebaSignIn-1)

- [raindrop-hb/tencent-video](https://github.com/raindrop-hb/tencent-video)

  

本项目基于以上项目开发，感谢支持。



---



## 🚔声明

**本项目仅供学习研究，请勿滥用！下载后请于24小时内删除，多谢合作！**

