import OlivOS
import OlivaBilibiliPlugin

from io import BytesIO
from PIL import Image
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

    def __str__(self):
        if self.isLegal():
            output = self.name + "[" + self.sex + "]" + "[LV" + str(self.level) + "]\n"
            output += self.sign
            return output
        else:
            return "用户不存在"
    
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

    def __str__(self):
        if self.isLegal():
            output = "[" + self.bvid + "]" + "[" + str(self.cid) + "]" + "[" + str(self.aid) + "]" + "\n"
            output += "标题：" + self.title + "\n"
            output += "分区：" + self.tname + "\n"
            output += "封面链接：" + self.pic + "\n"
            output += "发布时间：" + str(self.pubdate) + "\n"
            output += "投稿时间：" + str(self.ctime) + "\n"
            output += "简介：" + self.desc + "\n"
            output += "点赞投币收藏：" + str(self.state['like']) + "-" + str(self.state['coin']) + "-" + str(self.state['favorite']) + "\n"
            output += "分区：" + self.tname + "\n"
            pic = LoadImg(self.pic)
            pic.show()
            return output
        else:
            return "视频信息加载失败"

    def isLegal(self):
        return self.islegal
    
    def getVideoInfo(self):
        if self.isLegal():
            output = "[" + self.bvid + "]" + "\n" #"[" + str(self.cid) + "]" + "[" + str(self.aid) + "]" + 
            output += "[CQ:image,file=" + self.pic + "]\n"
            output += "标题：" + self.title + "\n"
            output += "分区：" + self.tname + "\n"
            output += "发布时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime(self.pubdate)) + "\n"
            output += "投稿时间：" + time.strftime("%Y-%m-%d %H:%M", time.localtime(self.ctime)) + "\n"
            output += "简介：" + self.desc + "\n"
            output += "点赞投币收藏：" + str(self.state['like']) + "-" + str(self.state['coin']) + "-" + str(self.state['favorite']) + "\n"
            output += "分区：" + self.tname + "\n"
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







#bili = BILIUSER()
#bili.getUserDatabyRoomId(5151978)
#bili.getUserDatafromApi()
#print(bili.room_init['uid'])

#LoadImg("http://i0.hdslb.com/bfs/face/74901f0be234adb631be1faead5c872974733d85.jpg").show()

#v = VIDEO(0 ,891716205)
#v.getVideoDataFromApi("aid")
#print(v)





