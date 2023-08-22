<p align="center">
  <h2 align="center"><storng>腾讯视频自动签到</storng></h2>
</p>


---



## 🥗腾讯视频使用说明
- 配置`config.cfg`配置文件中的  LOGIN_COOKIE 、LOGIN_URL、 LOGIN_URL_PAYLOADLOAD、PUSHPLUS_TOKEN、GET_VIP_INFO_URL_PAYLOAD几个参数，对象调用方法即可使用。
- TencentVideo对象提供三个方法：
  - tencent_video_auto_sign()：自动签到函数
  - tencent_video_get_vip_info()：查询会员信息
    - 这个方法还会领取一小时V力值任务【前提已完成，否则为0】
    - uId为不同用户标识，配置文件中自定义


---



## 🧶爱奇艺使用说明

- 配置`config.cfg`配置文件中的 `iqy_login_cookie`,对象掉方法既可以使用。
- IQY对象提供三个方法：
  - get_user_info():获取爱奇艺会员信息
  - get_rewards():领取已完成的每日任务

---



## 🥯如何抓取COOKIE

- 打开`https://v.qq.com/`扫码登陆
- 登陆成功后打开链接`https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2`,用开发者模式复制COOKIE即可，下图红色箭头指向的部分就是COOKIE

![](https://typora-1308603129.cos.ap-shanghai.myqcloud.com/typora/20220613193125.png)

- 成功运行推送如下图所示

![](https://typora-1308603129.cos.ap-shanghai.myqcloud.com/typora/20220613193904.png)

1. 或者登录成功之后F12，F5依次输入，然后搜索NewRefresh，这个url就是`LOGIN_URL`， `LOGIN_URL_PAYLOADLOAD`就是这个url的请求体。
2. `PUSHPLUS_TOKEN`公众号pushplus获取

> 注意：如果报错没有通过图像验证，需要在cookie中加入vdevice_qimei36='...'[使用常用手机打开获取](https://m.v.qq.com/schemeurl)

7. `GET_VIP_INFO_URL_PAYLOAD`[同样方法获取该链接的请求体](https://vip.video.qq.com/rpc/trpc.query_vipinfo.vipinfo.QueryVipInfo/GetVipUserInfoH5)
7. 爱奇艺的iqy_login_cookie同理，扫码登录[爱奇艺](https://iqyi.com)官网之后，点击[链接](http://serv.vip.iqiyi.com/vipgrowth/query.action)进入控制台查看cookie

---



## 📞注意事项

- 推送代码只写了PUSHPLUS的，可以自己拓展其他的推送
- 已经测试COOKIE有效时间超过三个月 目前还没过期

---



## ✨相似项目

- [bigoceans/TencentVideoAutoCheck](https://github.com/bigoceans/TencentVideoAutoCheck)
- [bigoceans/TencentVideoAutoCheck2.0](https://github.com/bigoceans/TencentVideoAutoCheck2.0)
- [raindrop-hb/tencent-video](https://github.com/raindrop-hb/tencent-video)

本项目基于以上项目开发，感谢支持。

---



## 🚔声明

**本项目仅供学习研究，请勿滥用！下载后请于24小时内删除，多谢合作！**

