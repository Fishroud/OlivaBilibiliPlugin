<div align="center">
  
```
 ██████╗ ██╗     ██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗     ██╗
██╔═══██╗██║     ██║██║   ██║██╔══██╗██╔══██╗██║██║     ██║
██║   ██║██║     ██║██║   ██║███████║██████╔╝██║██║     ██║
██║   ██║██║     ██║╚██╗ ██╔╝██╔══██║██╔══██╗██║██║     ██║
╚██████╔╝███████╗██║ ╚████╔╝ ██║  ██║██████╔╝██║███████╗██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝
```
# OLIVABILI - 基于OlivOS下的bilibili插件

</div>
<h3 align="center">不断更新中....</h3>

<div align="center">

本项目旨在基于OlivOS框架下实现对bilibili各类信息的解析和监控，以插件的形式存在并可跨平台使用
  
</div>

## 开始使用

**在使用前请安装额外依赖：Pillow**
> pip install Pillow

将opk文件放入\OlivOS\plugin\app目录下


## 触发指令

>/up [-u|--uid] uid

通过uid来查询用户基本信息

>/up [-r|--roomid] roomid

通过房间号来查询用户基本信息

>/video [-b|--bvid] bvid

通过bv号来查询视频基本信息

>/video [-a|--aid] aid

通过av号来查询视频基本信息

**注意：标准的av号不带av前缀**

>BV(\w{10})

发送一个bv号来查询视频基本信息

**注意：这是一个模糊匹配，任何带有合法bvid的单行消息都将被解析并发送（如url）**

>https://space.bilibili.com/uid
>
>https://live.bilibili.com/roomid

发送一个个人主页链接或者直播间链接来获取用户或直播间信息

## 其他

依赖项目：[OlivOS-Team / OlivOS](https://github.com/OlivOS-Team/OlivOS)

资料来源：[SocialSisterYi / bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
