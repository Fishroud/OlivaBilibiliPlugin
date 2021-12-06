import OlivOS
import OlivaBilibiliPlugin


def unity_reply(plugin_event, Proc):
    command_list = deleteBlank(plugin_event.data.message)
    if command_list[0].lower() == "/bilibili":
        if len(command_list) > 1 and command_list[1].isdigit():
            biliUser = OlivaBilibiliPlugin.bilibili.BILIUSER(int(command_list[1]))
            plugin_event.reply(biliUser.getUserInfo())
            save_path = OlivaBilibiliPlugin.main.run_path + "/plugin/data/OlivaBilibiliPlugin/" + str(biliUser.mid) + ".PNG"
            cqcode = "[CQ:image,file=file///" + save_path + "]"
            #plugin_event.reply(cqcode)
        else:
            plugin_event.reply("参数[uid]非法")

def deleteBlank(str):
    str_list = list(filter(None,str.split(" ")))
    return str_list