<p align="center">
  <h2 align="center"><storng>腾讯视频签到云函数</storng></h2>
</p>



## 🥗使用说明
- 配置`config.cfg`配置文件中的  LOGIN_COOKIE 、LOGIN_URL、 LOGIN_URL_PAYLOADLOAD、PUSHPLUS_TOKEN、GET_VIP_INFO_URL_PAYLOAD参数。
- 提供三个个方法：
  - tencent_video_auto_sign("uId")：自动签到函数
  - tencent_video_get_vip_info("uId")：查询会员信息
    - 这个方法还会领取一小时V力值任务【前提已完成，否则为0】
    - uId为不同用户标识，配置文件中自定义


## 🥯如何抓取COOKIE

- 打开`https://v.qq.com/`扫码登陆
- 登陆成功后打开链接`https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2`,用开发者模式复制COOKIE即可，下图红色箭头指向的部分就是COOKIE

![](https://typora-1308603129.cos.ap-shanghai.myqcloud.com/typora/20220613193125.png)

- 成功运行推送如下图所示

![](https://typora-1308603129.cos.ap-shanghai.myqcloud.com/typora/20220613193904.png)

1. 或者登录成功之后F12，F5依次输入，然后搜索NewRefresh，这个url就是`LOGIN_URL`， `LOGIN_URL_PAYLOADLOAD`就是这个url的请求体。
2. `PUSHPLUS_TOKEN`公众号pushplus获取

> 注意：如果报错没有通过图像验证，需要在cookie中加入vdevice_qimei36='...'[使用常用手机打开获取](https://m.v.qq.com/schemerul)

7. `GET_VIP_INFO_URL_PAYLOAD`[同样方法获取该链接的请求体](https://vip.video.qq.com/rpc/trpc.query_vipinfo.vipinfo.QueryVipInfo/GetVipUserInfoH5)



## 📞注意事项

- 推送代码只写了PUSHPLUS的，可以自己拓展其他的推送
- 已经测试COOKIE有效时间超过三个月 目前还没过期





## 🚔声明

**本项目仅供学习研究，请勿滥用！下载后请于24小时内删除，多谢合作！**

