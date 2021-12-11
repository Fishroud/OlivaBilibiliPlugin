'''
 ██████╗ ██╗     ██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗     ██╗
██╔═══██╗██║     ██║██║   ██║██╔══██╗██╔══██╗██║██║     ██║
██║   ██║██║     ██║██║   ██║███████║██████╔╝██║██║     ██║
██║   ██║██║     ██║╚██╗ ██╔╝██╔══██║██╔══██╗██║██║     ██║
╚██████╔╝███████╗██║ ╚████╔╝ ██║  ██║██████╔╝██║███████╗██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝
@File      :   OlivaBilibiliPlugin/msgReply.py
@Author    :   Fishroud鱼仙
@Contact   :   fishroud@qq.com
@Desc      :   None
'''
import OlivOS
import OlivaBilibiliPlugin

import os
import re

def unity_reply(plugin_event, Proc):


    command_list = deleteBlank(plugin_event.data.message)
    matchBV = re.match( r'^.*BV(\S{10}).*$', command_list[0], re.I)
    matchUrl = re.match( r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', command_list[0])
    image_path = os.path.abspath(OlivaBilibiliPlugin.data.save_path).replace("\\","\\\\")

    if len(command_list) == 1:
        if command_list[0].lower() == "/bilibili":
            plugin_event.reply("OlivaBilibiliPlugin by Fishroud")
        elif matchBV:
            bvid = matchBV.group(1)
            video = OlivaBilibiliPlugin.bilibili.VIDEO(bvid)
            video.getVideoDataFromApi()
            response = video.getVideoInfo()
            if response != "视频查询失败":
                plugin_event.reply(response)
        elif matchUrl:
            url = OlivaBilibiliPlugin.bilibili.URL(matchUrl.group(0))
            if url.netloc == "live.bilibili.com":
                if url.path_list[0].isdigit():
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER()
                    biliUser.getUserDatabyRoomId(int(url.path_list[0]))
                    biliUser.getUserDatafromApi()
                    response = biliUser.getLiveInfo()
                    if response != "用户不存在":
                        #save_path = image_path + "\\" + str(biliUser.mid) + ".PNG"
                        #cqcode = "[CQ:image,file=file:///" + save_path + "]"
                        plugin_event.reply("发现了bilibili直播房间链接！\n" + response)
                        del url,biliUser
            elif url.netloc == "space.bilibili.com":
                if url.path_list[0].isdigit():
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER(int(url.path_list[0]))
                    response = biliUser.getUserInfo()
                    if response != "用户不存在":
                        save_path = image_path + "\\" + str(biliUser.mid) + ".PNG"
                        cqcode = "[CQ:image,file=file:///" + save_path + "]"
                        plugin_event.reply(response + cqcode)
                        del url,biliUser
            elif url.netloc == "b23.tv":
                pass

    if len(command_list) == 2:
        if command_list[0].lower() == "/search":
            response = OlivaBilibiliPlugin.bilibili.searchUserByName(command_list[1])
            plugin_event.reply(response)



    if len(command_list) == 3:
        if command_list[0].lower() == "/up":
          #command_list[2].isdigit():
            if command_list[1].lower() == "--uid" or command_list[1].lower() == "-u":
                if command_list[2].isdigit():
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER(int(command_list[2]))
                    save_path = image_path + "\\" + str(biliUser.mid) + ".PNG"
                    cqcode = "[CQ:image,file=file:///" + save_path + "]"
                    plugin_event.reply(biliUser.getUserInfo() + cqcode)
                else:
                    plugin_event.reply("[--uid]的参数非法")
            elif command_list[1].lower() == "--roomid" or command_list[1].lower() == "-r":
                if command_list[2].isdigit():
                    biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER()
                    biliUser.getUserDatabyRoomId(int(command_list[2]))
                    biliUser.getUserDatafromApi()
                    save_path = image_path + "\\" + str(biliUser.mid) + ".PNG"
                    cqcode = "[CQ:image,file=file:///" + save_path + "]"
                    plugin_event.reply(biliUser.getUserInfo() + cqcode)
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









def deleteBlank(str):
    str_list = list(filter(None,str.split(" ")))
    return str_list