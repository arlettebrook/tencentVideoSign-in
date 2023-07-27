# 腾讯视频签到云函数

## 使用说明
- 修改`config.py`配置文件中的 COOKIE，和PUSHPLUS的TOKEN

## 如何抓取COOKIE

- 打开`https://v.qq.com/`扫码登陆
- 登陆成功后打开链接`https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2`,用开发者模式复制COOKIE即可，下图红色箭头指向的部分就是COOKIE

![](https://typora-1308603129.cos.ap-shanghai.myqcloud.com/typora/20220613193125.png)

- 成功运行推送如下图所示

![](https://typora-1308603129.cos.ap-shanghai.myqcloud.com/typora/20220613193904.png)

## 注意事项
- 推送代码只写了PUSHPLUS的，可以自己拓展其他的推送
- 已经测试COOKIE有效时间超过三个月 目前还没过期