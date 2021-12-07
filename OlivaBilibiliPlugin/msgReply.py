import OlivOS
import OlivaBilibiliPlugin


def unity_reply(plugin_event, Proc):
    command_list = deleteBlank(plugin_event.data.message)
    if command_list[0].lower() == "/bilibili":
        if len(command_list) == 1:
            plugin_event.reply("OlivaBilibiliPlugin by Fishroud")
        elif len(command_list) == 3:  #command_list[2].isdigit():
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








def deleteBlank(str):
    str_list = list(filter(None,str.split(" ")))
    return str_list