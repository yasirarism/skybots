#!usr/bin/python
# -*- coding: utf-8 -*-
import json
from .session import Session


class LiveClient(Session):

    def __init__(self, app = None):
        Session.__init__(self, app)
        self.database = json.load(open("database.json", "r"))

    def getMangoUser(self, userId):
        data = {
            "adid": "beea19ddc1c4dc6b",
            "build": 141,
            "channel": "official",
            "imei": "560157959697422",
            "language": "en",
            "device": "Redmi Note 4(7.0)",
            "platform": "Android",
            "region": "GB",
            "version": "1.4.1",
            "params": {
                "tid": userId
            }
        }
        try:r = self.request("POST", self.host_url + "/user/get", content = json.dumps(data), headers = self.headers)
        except:r = self.request("POST", self.host_url + "/user/get", data = json.dumps(data), headers = self.headers)
        if r.status_code == 200:
            data = r.json().get("data")
            if not data:
                return json.dumps({"code": 404, "reason": "F_Unknown result!", "result": "user id is not found!", "author": "Psychopumpum"})
            if data.get("user"):
                users  = data.get("user")
                result = {
                    "code": 200,
                    "name": users.get("name"),
                    "country": users.get("country"),
                }
                if data.get("live"):
                    live = data.get("live")
                    result.update({
                        "online": True,
                        "title": live.get("title"),
                        "thumbnail": live.get("coverUrl"),
                        "secret": live.get("secret"),
                        "price": live.get("price")
                    })
                    if not live.get("secret"):
                        result.update({"stream_url": live.get("pullUrlList", [])[0]})
                else:
                    result.update({"online": False, "thumbnail": users.get("head")})
                return json.dumps(result)
            return json.dumps({"code": 404, "online": False, "result": "Invalid id parameter!", "author": "Psychopumpum"})
        return json.dumps({'code': 404, "online": False, "result": "Unknown result!", "author": "Psychopumpum"})

    def getThai69LiveUser(self, room_id):
        data = {"room_id": room_id}
        r = self.request("POST", self.host_url + "/intem-live/index/user_video_async", content = json.dumps(data), headers = self.headers)
        if r.status_code == 200:
            data = r.json()
            if data.get("code") == 200:
                data = data.get('data')
                result = {
                    "code": 200,
                    "name": data.get("nickName"),
                    "online": data.get("online_status"),
                    "title": data.get("group_id"),
                    "secret": False if not data.get("is_live_pay") else True,
                    "price": data.get("is_live_fee", 0)
                }
                try:
                    r = self.request("GET", data.get("head_image"), headers = {"User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; Redmi Note 4 MIUI/V11.0.2.0.NCFMIXM)"})
                    if r.status_code == 200:
                        with open(f"{room_id}.jpg", "wb") as fp:
                            fp.write(r.content)
                        result.update({"thumbnail": f"{room_id}.jpg"})
                    else:
                        result.update({"thumbnail": None})
                except:
                    result.update({"thumbnail": None})
                return json.dumps(result)
            return json.dumps({"code": 404, "online": False, "result": "Invalid id parameter!", "author": "Psychopumpum"})
        return json.dumps({"code": 404, "online": False, "result": "Unknown result!", "author": "Psychopumpum"})

    def getHoneyRecommended(self, page = 1):
        params = {"page": page}
        r = self.request('GET', self.host_url + "/App/Live/RecommendList", params = params, headers = self.headers)
        if r.status_code == 200 and not (r.json().get("code") and r.json().get("msg")):
            result = r.json().get("result")
            result = [
                {
                    "code": 200,
                    "city": data.get("city"),
                    "title": data.get("title"),
                    "name": data.get("nickname"),
                    "price": data.get("price"),
                    "secret": True if float(data.get('price')) else False,
                    "thumbnail": f"https://stdn-android.bugly.qq.com/{data.get('cover')}" if data.get('cover') else None,
                    "live_id": data.get("cover").replace("live/cover/20211209/", "").split("_")[1].replace(".png", "") if data.get("cover") else None,
                } for data in result
            ]
            return json.dumps(result, indent = 4)
        return json.dumps({"code": 404, "result": []})

    def getHoneyLiveUser(self, id):
        data   = json.loads(self.getHoneyRecommended())
        result = list(filter(lambda m: m.get("live_id") == id, data))
        page   = 2
        while not result:
            data   = json.loads(self.getHoneyRecommended(page))
            result = list(filter(lambda m: m.get("live_id") == id, data))
            page  += 1
            if not data:
                break
        if not result:
            return json.dumps({"code": 404, "result": "Unknown maybe host offline"})
        return json.dumps(result[0])

    def getDatabaseLiveUser(self, id, app = "SugarLive"):
        if self.database.get(id):
            data = self.database.get(id)
        elif self.database.get(id[1:]):
            data = self.database.get(id[1:])
        else:
            data = None
        if not data:
            return json.dumps({"code": 200, "name": "Unknown", "title": "Unknown", "id": id, "app": app})
        return json.dumps({"code": 200, "name": data.get("nickname"), "host": data.get("host"), "id": data.get("user_id"), "app": app})