import OlivOS
import OlivaBilibiliPlugin

import os

global save_path
save_path = "./plugin/data/OlivaBilibiliPlugin"

global run_path
run_path = "C:/Users/86178/source/repos/OlivOS"

class Event(object):
    def init(plugin_event, Proc):        
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        pass

    def private_message(plugin_event, Proc):
        OlivaBilibiliPlugin.msgReply.unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        OlivaBilibiliPlugin.msgReply.unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        pass

    def save(plugin_event, Proc):
        pass

