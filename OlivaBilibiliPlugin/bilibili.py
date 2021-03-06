'''
 ██████╗ ██╗     ██╗██╗   ██╗ █████╗ ██████╗ ██╗██╗     ██╗
██╔═══██╗██║     ██║██║   ██║██╔══██╗██╔══██╗██║██║     ██║
██║   ██║██║     ██║██║   ██║███████║██████╔╝██║██║     ██║
██║   ██║██║     ██║╚██╗ ██╔╝██╔══██║██╔══██╗██║██║     ██║
╚██████╔╝███████╗██║ ╚████╔╝ ██║  ██║██████╔╝██║███████╗██║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝
@File      :   OlivaBilibiliPlugin/bilibili.py
@Author    :   Fishroud鱼仙
@Contact   :   fishroud@qq.com
@Desc      :   None
'''

import OlivOS
import OlivaBilibiliPlugin

from io import BytesIO
from PIL import Image
import urllib.parse
import requests
import json
import base64
import time



class BILIUSER:
    def __init__(self ,mid = 0):
        self.mid = mid
        self.name = None
        self.sex = None
        self.face_url = None
        self.live_key_frame = None
        self.sign = None
        self.level = None
        self.silence = None
        self.fans = {}
        self.vip = {}
        self.pendant = {}
        self.live = {}
        self.room_init = {}
        self.islegal = False
        if mid != 0:
            self.getUserDatafromApi()
            self.getUserDatabyRoomId(self.live['roomid'])



    def getUserDatafromApi(self):
        if self.mid != 0:
            api = "http://api.bilibili.com/x/space/acc/info?mid=" + str(self.mid)
            payload={}
            headers = {
              'Cookie': 'LIVE_BUVID=AUTO2616196871676659'
            }
            response = requests.request("GET", api, headers=headers, data=payload)
            userjson = json.loads(response.text)
            if userjson['code'] == 0:
                self.name = userjson['data']['name']
                self.sex = userjson['data']['sex']
                self.face_url = userjson['data']['face']
                self.sign = userjson['data']['sign']
                self.level = userjson['data']['level']
                self.silence = userjson['data']['silence']
                self.fans = userjson['data']['fans_medal']
                self.vip = userjson['data']['vip']
                self.pendant = userjson['data']['pendant']
                self.live = userjson['data']['live_room']
                self.islegal = True
        return


    def getUserDatabyRoomId(self ,roomid):
        api = "http://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(roomid)
        payload={}
        headers = {
          'Cookie': 'LIVE_BUVID=AUTO2616196871676659'
        }
        response = requests.request("GET", api, headers=headers, data=payload)
        userjson = json.loads(response.text)
        if userjson['code'] == 0:
            self.mid = userjson['data']['uid']
            self.room_init = userjson['data']
        return


    def getUserLiveStatusbyUids(self ,uid_list = []):
        if not uid_list:
            uid_list.append(self.mid)
        api = "https://api.live.bilibili.com/room/v1/Room/get_status_info_by_uids"
        payload = json.dumps({
          "uids": uid_list
        })
        headers = {
          'Content-Type': 'application/json',
          'Cookie': 'LIVE_BUVID=AUTO2616196871676659'
        }
        response = requests.request("POST", api, headers=headers, data=payload)
        userjson = json.loads(response.text)
        if userjson['code'] == 0:
            self.live_key_frame = userjson['data'][self.mid]['keyframe']

    def isLegal(self):
        return self.islegal
    
    def userInfoImage(self):
        if self.isLegal():
            face_image = LoadImg(self.face_url)
            background = Image.new('RGBA' ,(420,420))
            face_image.thumbnail((220,220))
            face_image = face_image.convert('RGBA')
            background.paste(face_image ,(100,100))
            if self.pendant['image'] != "":
                pendant_image = LoadImg(self.pendant['image'])
                pendant_image = pendant_image.convert('RGBA')
                r,g,b,a = pendant_image.split()
                background.paste(pendant_image ,(0,0) ,mask = a)
            #background.show()
            
            '''
            output_buffer = BytesIO()
            background.save(output_buffer, format='PNG')
            byte_data = output_buffer.getvalue()
            base64_str = base64.b64encode(byte_data).decode('utf-8')
            '''
            save_path = OlivaBilibiliPlugin.data.save_path + "/" + str(self.mid) + ".PNG"
            background.save(save_path)
        #return base64_str
        return

    def getUserInfo(self):
        if self.isLegal():
            output = self.name + "[" + self.sex + "]" + "[LV" + str(self.level) + "]\n"
            output += self.sign
            self.userInfoImage()
            return output
        else:
            return "用户不存在"
        
    def getLiveInfo(self):
        if self.isLegal():
            output = "该主播当前"
            if self.live['liveStatus'] != 0:
                output += "正在直播\n"
                output += "开播时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime(self.room_init['live_time'])) + "\n"
            else:
                output += "未在直播\n"
            output += self.name + "[" + str(self.mid) + "]" + "\n"
            output += "https://live.bilibili.com/" + str(self.live['roomid']) + "\n"
            output += "标题：" + self.live['title'] + "\n"
            output += "[OP:image,file=" + self.live['cover'] + "]\n"
            return output
        else:
            return "用户不存在"



class VIDEO:
    def __init__(self ,bvid = "0" ,aid = 0):
        self.bvid = bvid
        self.aid = aid
        self.cid = None
        self.tname = None
        self.pic = None
        self.title = None
        self.pubdate = None
        self.ctime = None
        self.desc = None
        self.nowWatching = None
        self.owner = {}
        self.state = {}
        self.first_frame = None
        self.islegal = False

    def getVideoDataFromApi(self ,type = "bvid"):
        if type == "bvid":
            url = "http://api.bilibili.com/x/web-interface/view?bvid=" + self.bvid
        elif type == "aid":
            url = "http://api.bilibili.com/x/web-interface/view?aid=" + str(self.aid)
        payload={}
        headers = {
          'Cookie': 'LIVE_BUVID=AUTO2616196871676659'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        videojson = json.loads(response.text)
        if videojson['code'] == 0:
            self.bvid = videojson['data']['bvid']
            self.aid = videojson['data']['aid']
            self.cid = videojson['data']['cid']
            self.tname = videojson['data']['tname']
            self.pic = videojson['data']['pic']
            self.title = videojson['data']['title']
            self.pubdate = videojson['data']['pubdate']
            self.ctime = videojson['data']['ctime']
            self.desc = videojson['data']['desc']
            self.owner = videojson['data']['owner']
            self.state = videojson['data']['stat']
            #self.first_frame = videojson['data']['pages'][0]['first_frame']
            self.islegal = True
        api = "https://api.bilibili.com/x/player/online/total?cid="+ str(self.cid) + "&bvid=" + str(self.bvid)
        payload={}
        headers = {
          'Cookie': 'LIVE_BUVID=AUTO2616196871676659'
        }
        response = requests.request("GET", api, headers=headers, data=payload)
        responsejson = json.loads(response.text)
        if responsejson['code'] == 0:
            self.nowWatching = responsejson['data']['total']
        return


    def isLegal(self):
        return self.islegal

    def getVideoInfo(self):
        if self.isLegal():
            output = "[" + self.bvid + "]" + "\n" #"[" + str(self.cid) + "]" + "[" + str(self.aid) + "]" + 
            output += "[OP:image,file=" + self.pic + "]\n"
            output += "标题：" + self.title + "\n"
            output += "UP主：" + self.owner['name'] + "[" + str(self.owner['mid']) + "]\n"
            output += "分区：" + self.tname + "\n"
            output += "发布时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime(self.pubdate)) + "\n"
            output += "投稿时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime(self.ctime)) + "\n"
            if self.desc == "":
                output += "简介： - \n"
            else:
                output += "简介：" + self.desc + "\n"
            output += "点赞投币收藏：" + str(self.state['like']) + "-" + str(self.state['coin']) + "-" + str(self.state['favorite']) + "\n"
            output += "播放数量：" + str(self.state['view']) + "\n"
            output += "在线观看人数：" + str(self.nowWatching) + "\n"
            output += "链接：https://www.bilibili.com/video/"+ self.bvid
            return output
        else:
            return "视频查询失败"







def LoadImg(img_url):
    header = {}
    response = requests.get(img_url, headers=header, stream=True)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    del response



class URL:
    def __init__(self, url):
        self.url = url
        self.netloc = None
        self.sheme = None
        self.path = None
        self.path_list = []
        self.query = {}
        self.analyseUrl()


    def analyseUrl(self):
        self.netloc = urllib.parse.urlsplit(self.url).netloc
        self.sheme = urllib.parse.urlsplit(self.url).scheme
        self.path = urllib.parse.urlsplit(self.url).path
        self.query = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.url).query))
        self.path_list = self.path2list()
        return

    def path2list(self):
        path_list = list(filter(None,self.path.split("/")))
        return path_list
    
    def getHtml(self):
        url = self.url
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
        return response.text


def searchUserByName(name):
    name = urllib.parse.quote(name)
    api = "https://api.bilibili.com/x/web-interface/search/type?context=&search_type=bili_user&page=1&order=&keyword=" + name + "&category_id=&user_type=&order_sort=&changing=mid&__refresh__=true&_extra=&highlight=1&single_column=0"
    payload={}
    headers = {
      'Cookie': 'LIVE_BUVID=AUTO2616196871676659'
    }
    response = requests.request("GET", api, headers=headers, data=payload)
    searchjson = json.loads(response.text)
    if searchjson['code'] == 0:
        output = "共查找到" + str(searchjson['data']['numResults']) + "条记录\n"
        if searchjson['data']['numResults'] == 0:
            return output
        search_result_list = searchjson['data']['result']
        if len(search_result_list) > 5:
            output += "由于条数过多，将优先显示前五条\n"
            search_result_list = search_result_list[:5]
        for search_result_this in search_result_list:
            output += "[OP:image,file=https:" + search_result_this['upic'] + "]\n"
            output += search_result_this['uname'] + "[" + str(search_result_this['mid']) + "][LV" + str(search_result_this['level']) + "]\n"
            if search_result_this['usign'] == "":
                output += "此用户没有个性签名啊( `д´)\n"
            else:
                output += search_result_this['usign'] + "\n"
            output += "视频数：" + str(search_result_this['videos']) + "，粉丝数：" + str(search_result_this['fans']) + "\n"
        return output
    else:
        output = "查询失败( ﾟA。)"
        return output

