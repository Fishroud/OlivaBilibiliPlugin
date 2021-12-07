mport OlivOS
import OlivaBilibiliPlugin

import re

def unity_reply(plugin_event, Proc):
    command_list = deleteBlank(plugin_event.data.message)
    plugin_event.reply(str(command_list))
    if command_list[0].lower() == "/bilibili":
        if len(command_list) == 1:
            plugin_event.reply("OlivaBilibiliPlugin by Fishroud")
    elif command_list[0].lower() == "/up":
        if len(command_list) == 3:  #command_list[2].isdigit():
            if command_list[1].lower() == "--uid" or command_list[1].lower() == "-u":
                if command_list[2].isdigit():
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER(int(command_list[2]))
                    plugin_event.reply(biliUser.getUserInfo())
                    save_path = OlivaBilibiliPlugin.main.run_path + "/plugin/data/OlivaBilibiliPlugin/" + str(biliUser.mid) + ".PNG"
                    cqcode = "[CQ:image,file=file///" + save_path + "]"
                    #plugin_event.reply(cqcode)
                else:
                    plugin_event.reply("[--uid]的参数非法")
            elif command_list[1].lower() == "--roomid" or command_list[1].lower() == "-r":
                if command_list[2].isdigit():
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER()
                    biliUser.getUserDatabyRoomId(int(command_list[2]))
                    biliUser.getUserDatafromApi()
                    plugin_event.reply(biliUser.getUserInfo())
                else:
                    plugin_event.reply("[--roomid]的参数非法")
    elif command_list[0].lower() == "/video":
        if len(command_list) == 3:  #command_list[2].isdigit():
            if command_list[1].lower() == "--aid" or command_list[1].lower() == "-a":
                if command_list[2].isdigit():
                    video = OlivaBilibiliPlugin.bilibili.VIDEO(0 ,int(command_list[2]))
                    video.getVideoDataFromApi("aid")
                    plugin_event.reply(video.getVideoInfo())
                else:
                    plugin_event.reply("[--aid]的参数非法")
            elif command_list[1].lower() == "--bvid" or command_list[1].lower() == "-b":
                video = OlivaBilibiliPlugin.bilibili.VIDEO(command_list[2])
                video.getVideoDataFromApi()
                plugin_event.reply(video.getVideoInfo())
    elif command_list[0].lower() == "/biliurl":
            if len(command_list) == 2:  #command_list[2].isdigit():
                EnUrl,Av=EncodeUrl(command_list[1])
                juUrl=judgeUrl(command_list[1])
                if juUrl==0:
                    plugin_event.reply("已识别到长链接")
                    if Av==0:
                        video = OlivaBilibiliPlugin.bilibili.VIDEO(EnUrl)
                        video.getVideoDataFromApi()
                        plugin_event.reply(video.getVideoInfo())
                    else:
                        if EnUrl.isdigit():
                            video = OlivaBilibiliPlugin.bilibili.VIDEO(0 ,int(EnUrl))
                            video.getVideoDataFromApi("aid")
                            plugin_event.reply(video.getVideoInfo())
                        else:
                            plugin_event.reply("[--aid]的参数非法")
                elif  juUrl==1:
                    plugin_event.reply("已识别到短链接")
                    if Av==0:
                        video = OlivaBilibiliPlugin.bilibili.VIDEO(EnUrl)
                        video.getVideoDataFromApi()
                        plugin_event.reply(video.getVideoInfo())
                    else:
                        if EnUrl.isdigit():
                            video = OlivaBilibiliPlugin.bilibili.VIDEO(0 ,int(EnUrl))
                            video.getVideoDataFromApi("aid")
                            plugin_event.reply(video.getVideoInfo())
                        else:
                            plugin_event.reply("[--aid]的参数非法")
                elif  juUrl==2:
                    plugin_event.reply("已识别到直播间链接")
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER()
                    biliUser.getUserDatabyRoomId(int(EnUrl))
                    biliUser.getUserDatafromApi()
                    plugin_event.reply(biliUser.getUserInfo())
                elif  juUrl==3:
                    plugin_event.reply("已识别到人物主页链接")
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER(int(EnUrl))
                    plugin_event.reply(biliUser.getUserInfo())
                    save_path = OlivaBilibiliPlugin.main.run_path + "/plugin/data/OlivaBilibiliPlugin/" + str(biliUser.mid) + ".PNG"
                    cqcode = "[CQ:image,file=file///" + save_path + "]"




def deleteBlank(str):
    str_list = list(filter(None,str.split(" ")))
    return str_list


def judgeUrl(url):
    url=url.split("/")
    if url[2]=="www.bilibili.com":
        return 0
    elif url[2]=="b23.tv":
        return 1
    elif url[2]=="live.bilibili.com":
        return 2
    elif url[2]=="space.bilibili.com":
        return 3
    else:
        return 4
def EncodeUrl(url):
    judge=judgeUrl(url)
    av=0
    if judge == 0:
        try:
            re1=re.findall(r"https://www.bilibili.com/video/(.*?)[\?\/].*",url,re.S)[0]
        except:
            re1=re.findall(r"https://www.bilibili.com/video/(.*)",url,re.S)[0]
        finally:
            if re1[0:2].lower()=="av":
                re1=re1[2:]
                av=1
        return re1,av
    elif judge==1:
        try:
            re1=re1=re.findall(r"https://b23.tv/(.*?)[\?\/].*",url,re.S)[0]
        except:
            re1=re.findall(r"https://b23.tv/(.*)",url,re.S)[0]
        finally:
            if re1[0:2].lower()=="av":
                re1=re1[2:]
                av=1
        return re1,av
    elif judge==2:
        try:
            re1=re1=re.findall(r"https://live.bilibili.com/(.*?)[\?\/].*",url,re.S)[0]
        except:
            re1=re.findall(r"https://live.bilibili.com/(.*)",url,re.S)[0]
        return re1,av
    elif judge==3:
        try:
            re1=re1=re.findall(r"https://space.bilibili.com/(.*?)[\?\/].*",url,re.S)[0]
        except:
            re1=re.findall(r"https://space.bilibili.com/(.*)",url,re.S)[0]
        return re1,av
    else:
        return 
