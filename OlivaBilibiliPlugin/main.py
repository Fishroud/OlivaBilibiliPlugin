'''
 ██████╗ ██╗     ██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗     ██╗
██╔═══██╗██║     ██║██║   ██║██╔══██╗██╔══██╗██║██║     ██║
██║   ██║██║     ██║██║   ██║███████║██████╔╝██║██║     ██║
██║   ██║██║     ██║╚██╗ ██╔╝██╔══██║██╔══██╗██║██║     ██║
╚██████╔╝███████╗██║ ╚████╔╝ ██║  ██║██████╔╝██║███████╗██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝
@File      :   OlivaBilibiliPlugin/main.py
@Author    :   Fishroud鱼仙
@Contact   :   fishroud@qq.com
@Desc      :   None
'''
import OlivOS
import OlivaBilibiliPlugin

import os

class Event(object):
    def init(plugin_event, Proc):        
        if not os.path.exists(OlivaBilibiliPlugin.data.save_path):
            os.mkdir(OlivaBilibiliPlugin.data.save_path)
        pass

    def private_message(plugin_event, Proc):
        OlivaBilibiliPlugin.msgReply.unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        OlivaBilibiliPlugin.msgReply.unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        pass

    def save(plugin_event, Proc):
        pass

