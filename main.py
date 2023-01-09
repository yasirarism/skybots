#!usr/bin/python
# -*- coding: utf-8 -*-
from pyrogram import idle, Client, filters
from pyrogram.types import Message
from streamData import LiveClient
import time, asyncio, re, json, livejson

app = Client("helper", 19444956, "d0ccdf2432cf42a41e75179015c8baf1", bot_token = "5662215015:AAGPyGaAbKYFZB0CJPPUHvVSFmExBtZ4uSg")
settings = livejson.File('settings.json', True, True, 4)
ADMINS = json.load(open("newSettings.json", "r"))
bot_start = time.time()

with app:
    bots = app.get_me()
    username = f"@{bots.username.lower()}"

async def forward(c, m: Message, msg):
    data = json.load(open("newSettings.json", "r"))["author"]
    data = list(set(data))
    if m.from_user.id in data:
        data.remove(m.from_user.id)
    print(data)
    for chat in data:
        print(chat)
        try:
            await asyncio.sleep(2)
            a = await msg.forward(chat)
            print(a)
        except Exception as e:
            print(e)
            await asyncio.sleep(2)
            await c.send_message(chat, str(msg.text))
    return

@app.on_message(~filters.outgoing & ~filters.bot & filters.text)
async def getText(_, m: Message):
    if m.text.startswith("/"):
        text = str(m.text)
        if text.lower() == "/start" or text.lower() == f"/start{username}":
            msg = await m.reply_text("Subscribe: @BotXRecord\nIf you want to order bots.")
            if m.from_user.id in settings["admin"] or m.from_user.id in settings["author"]:
                await asyncio.sleep(1)
                return await msg.edit(f"Subscribe: @BotXRecord\nIf you want to order bots.\n\n/id **Get your identities**\n/Ping **Check Bots Response**")
        elif text.lower() == "/id" or text.lower() == f"/id{username}":
            return await m.reply_text(f"**UserID:** `{m.from_user.id}`")
        elif text.lower() == "/ping" or text.lower() == f"/ping{username}":
            s = time.time()
            msg = await m.reply_text("Fetching....")
            return await msg.edit(f"Took: {round((time.time()-s)*1000, 2)} ms")
        elif text.lower().startswith("/public") or text.lower().startswith(f"/public{username}"):
            txt = text[len("/public "):] if username.lower() not in text.lower() else text[len(f'/public{username} '):]
            if not txt:
                return
            elif txt.lower() == "on":
                settings["public"] = True
                return await m.reply_text("Public switch to on.")
            elif txt.lower() == "off":
                settings['public'] = False
                return await m.reply_text('Public switch to off.')
        elif text.lower().startswith("/admin"):
            userId = text[len("/admin "):]
            if not userId.isdigit():return await m.reply("Invalid user id.")
            data = json.load(open("newSettings.json", "r"))
            data["kntl"].append(int(userId))
            with open("newSettings.json", "w") as fp:
                json.dump(data, fp, indent = 4, sort_keys = True)
            return await m.reply("Userid added to admin.")
        elif text.lower() == "/restart":
            await m.reply_text("Restarting...")
            import sys, os
            arg = sys.executable
            os.execl(arg, arg, *sys.argv)
    elif not m.text.startswith("/"):
        text = str(m.text)
        ppp = json.load(open("newSettings.json", "r"))
        ADMIN = ppp.get("kntl") + ppp.get("author") + json.load(open("settings.json", "r")).get("admin")
        if not settings["public"]:
            if m.from_user.id not in ADMIN:
                return
        if "wstime" and "wssecret" in text.lower():
            urls = re.findall(r"(\d+_\d+)\?wsSecret=(\w+)\&wsTime=(\d+)", str(m.text))
            if urls and len(urls[0]) == 3:
                urls    = urls[0]
                url = f"rtmp://play001.chensimeng.cn/Fd8ctp/{urls[0]}?wsSecret={urls[1]}&wsTime={urls[2]}"
                url2 = f"rtmp://play001.dt01showxx07.com/d73lQ0/{urls[0]}?wsSecret={urls[1]}&wsTime={urls[2]}"
                url3 = f"rtmp://play01.kkkliveapp2.com/Cgl9zd/{urls[0]}?wsSecret={urls[1]}&wsTime={urls[2]}"
                cl = LiveClient("HONEY")
                uid = urls[0].split("_")[0]
                data = json.loads(cl.getHoneyLiveUser(uid))
                if data.get("code") == 404:
                    text = f"Name: **Unknown**\nID: **{uid}**\nAPP: **BLING²**\n\nURL:\n- `{url}` \n\n- `{url2}` \n\n- `{url3}`"
                elif data.get("code") == 200:
                    text = f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **BLING²**\n\nURL:\n- `{url}` \n\n- `{url2}` \n\n- `{url3}`"
                msg = await m.reply_text(text)
                await asyncio.sleep(2)
                return await forward(_, m, msg)
        if "wstime" and "wssecret" in text.lower():
            urls = re.findall(r"(\d+_\d+)\?wsSecret=(\w+)\&wsTime=(\d+)", str(m.text))
            if urls and len(urls[0]) == 3:
                urls    = urls[0]
                url = f"rtmp://play001.chensimeng.cn/Fd8ctp/{urls[0]}?wsSecret={urls[1]}&wsTime={urls[2]}"
                url2 = f"rtmp://play001.dt01showxx07.com/d73lQ0/{urls[0]}?wsSecret={urls[1]}&wsTime={urls[2]}"
                url3 = f"rtmp://play01.kkkliveapp2.com/Cgl9zd/{urls[0]}?wsSecret={urls[1]}&wsTime={urls[2]}"
                cl = LiveClient("HONEY")
                uid = urls[0].split("_")[0]
                data = json.loads(cl.getHoneyLiveUser(uid))
                if data.get("code") == 404:
                    text = f"Name: **Unknown**\nID: **{uid}**\nAPP: **BLING²**\n\nURL:\n- `{url}` \n\n- `{url2}` \n\n- `{url3}`"
                elif data.get("code") == 200:
                    text = f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **BLING²**\n\nURL:\n- `{url}` \n\n- `{url2}` \n\n- `{url3}`"
                msg = await m.reply_text(text)
                await asyncio.sleep(2)
                return await forward(_, m, msg)
        elif "sugar" in str(m.text.lower()):
            urls = re.findall(r"sugar\S+", str(m.text))
            if urls:
                urls = urls[0]
                url  = f"`rtmp://sg1.pul.sugarlive.me/sugar/{urls}`"
                user_id = urls.split("_")
                if user_id[1].isdigit():
                    uid = user_id[1]
                    cl = LiveClient("HONEY")
                    data = json.loads(cl.getDatabaseLiveUser(uid, "Sugar Live"))
                    text = f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **Sugar Live**\n\nURL: {url}"
                    msg = await m.reply_text(text)
                    await asyncio.sleep(2)
                    return await forward(_, m, msg)
        elif "mango" in str(m.text.lower()):
            urls = re.findall(r"mango\S+", m.text)
            if urls:
                urls = urls[0]
                url  = f"`rtmp://pull.rtmp.yogurtlive.me/mango/{urls}`"
                user_id = urls.split("_")
                if len(user_id) == 3 and user_id[1].isdigit():
                    uid = user_id[1]
                    cl = LiveClient("MANGO")
                    data = json.loads(cl.getMangoUser(uid))
                    if data.get('code') == 200:
                        text = f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **Mango Live**\n\nURL: {url}"
                    else:
                        text = f"Name: **Unknown**\nID: **{uid}**\nAPP: **Mango Live**\n\nURL: {url}"
                    msg = await m.reply_text(text)
                    await asyncio.sleep(2)
                    return await forward(_, m, msg)
        elif "auth_key" in str(m.text.lower()):
            urls = re.findall(r'(\d+\_\d\S+)', text)
            if urls:
                urls = urls[0]
                url  = f"`rtmp://sea1.live.fantasylive.cc/dreamlive/{urls}`"
                user_id = url.split("/dreamlive/")[1].split("_")[0]
                cl = LiveClient("Dream Live")
                data = json.loads(cl.getDatabaseLiveUser(user_id, 'Dream Live'))
                name, uid = data.get('name', "Unknown"), user_id
                text = f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **Dream Live**\n\nURL: {url}"
                msg = await m.reply_text(text)
                return await forward(_, m, msg)

if __name__ == '__main__':
    print("Bots has been running")
    app.start()
    idle()
