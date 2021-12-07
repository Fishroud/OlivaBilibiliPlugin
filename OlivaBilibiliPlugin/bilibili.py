import OlivOS
import OlivaBilibiliPlugin

from io import BytesIO
from PIL import Image
import requests
import json
import base64



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
        self.getUserDatafromApi()
        if mid != 0:
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
            pendant_image = LoadImg(self.pendant['image'])
            background = Image.new('RGBA' ,(420,420))
            face_image.thumbnail((220,220))
            face_image.convert('RGBA')
            pendant_image.convert('RGBA')
            r,g,b,a = pendant_image.split()
            background.paste(face_image ,(100,100))
            background.paste(pendant_image ,(0,0) ,mask = a)
            #background.show()
            
            '''
            output_buffer = BytesIO()
            background.save(output_buffer, format='PNG')
            byte_data = output_buffer.getvalue()
            base64_str = base64.b64encode(byte_data)
            '''
            save_path = OlivaBilibiliPlugin.main.save_path + "/" + str(self.mid) + ".PNG"
            background.save(save_path)
            return

    def getUserInfo(self):
        if self.isLegal():
            output = self.name + "[" + self.sex + "]" + "[LV" + str(self.level) + "]\n"
            output += self.sign
            return output
        else:
            return "用户不存在"


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









