# -*- coding: utf-8 -*-
import sys, asyncio, ffmpeg, livejson, json, re, os, types
from src import *
from pyrogram import Client, filters, idle
from pyrogram.enums import ChatType
from pyrogram.types import Message
from datetime import timedelta, datetime
from pytz import timezone
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from streamData import LiveClient
from os import environ
from dotenv import load_dotenv
import logging

load_dotenv("config.env", override=True)

AUTHOR_ID = list({int(x) for x in environ.get("AUTHOR_ID").split()})
SESSION_NAME = environ.get("SESSION_NAME", "skybots")
MAX_LINK = environ.get("MAX_LINK", 4)
TOKEN = environ.get("TOKEN")

settings = livejson.File(f"database/skybots.json", True, True, 4)
if not settings:
    settings.update({
        "author": AUTHOR_ID,
        "url": {},
        "limit": 0
    })
elif settings["url"]:
    for k, v in settings["url"].items():
        if os.path.isfile(v["name"]):os.remove(v["name"])
    settings["url"] = {}
    
if isinstance(list, types.ModuleType):
    del list
    logging.info("List deleted..")
logging.info(f"Type list is: {list.__name__}")

database  = json.load(open("settings.json", "r"))
client    = Client(f"session/{SESSION_NAME}", api_id = database["api_id"], api_hash = database["api_hash"], bot_token = TOKEN)
loop      = asyncio.get_event_loop()
watermark = "Subscribe: @StreamingXBot" if 692043981 not in AUTHOR_ID else "Author: @FadhilvanHalen"
if 692043981 in AUTHOR_ID:
    settings['limit'] = 999
else:
    settings['limit'] = MAX_LINK

async def run_command(*args, _msg = None, _url = None, name = None):
    data = len(settings["url"])
    if data >= settings['limit']:
        if _msg:
            return await _msg.edit(f"You can't record anymore, max link is only {settings['limit']} and already used.")
    if _url:
        if _url not in settings["url"]:
            settings["url"][_url] = {
                "status": True,
                "name": name
            }
        else:
            return await _msg.edit(f"This `{_url}` is already recorded, please chose another one.")
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        return (name, stdout.decode("utf-8").strip())
    else:
        if _url:
            if os.path.isfile(name):
                try:del settings["url"][_url]
                except KeyError:pass
                return (name, stderr.decode("utf-8").strip())
            del settings["url"][_url]
        if _msg:
            return await _msg.edit("Host is already offline or link not valid.")
        return (name, stderr.decode("utf-8").strip())
    return (name, stdout.decode("utf-8").strip())

async def delete(m):
    try:await m.delete()
    except:pass

async def send_video(_, m, result, c: str):
    filename, result_ = result[0], result[1]
    if filename and os.path.isfile(filename):
        video = await run_command("ffmpeg", "-i", filename, "-codec", "copy", "-y", filename.replace('.flv', '.mp4'))
        name  = filename.replace(".flv", "")
        if os.path.isfile(filename):
            os.remove(filename)
        video = ffmpeg.probe(f"{name}.mp4")
        if video.get('format'):
            dur, size = video["format"].get("duration", 0), video["format"].get("size", 0)
        else:
            dur, size = 600, 300
        end, duration = 3600, int(float(dur))
        videos = []
        for i in range(0, duration, end):
            ffmpeg_extract_subclip(f"{name}.mp4", i, end, f"{name}_{i}.mp4")
            videos.append(f'{name}_{i}.mp4')
            i += end
            end += 3600
            if end > duration:
                erm = end - duration
                end = end - erm
        start = datetime.now(timezone("Asia/Jakarta"))
        caption = f"{watermark}\n{start.strftime('%d %b %Y')}"
        thums = []
        for no, path in enumerate(videos, start = 1):
            vid = ffmpeg.probe(path)
            dur = int(float(vid['format']['duration']))
            thumb = await run_command("ffmpeg", "-i", path, "-vframes", "1", "-an", "-ss", "00", "-y", path.replace(".mp4", ".png"))
            thums.append(path.replace(".mp4", ".png"))
            mm = await m.reply_video(path, True, caption = caption, duration = dur, width = int(float(vid["streams"][0]["width"])), height = int(vid["streams"][0]["height"]), thumb = path.replace('.mp4', '.png'))
            try:msss = await _.send_video(database['author'][0], path, caption, duration = dur, thumb = path.replace('.mp4', '.png'))
            except:msss = None
            print(msss)
            os.remove(path)
        if os.path.isfile(f"{name}.mp4"):os.remove(f"{name}.mp4")
        for t_ in thums:
            if os.path.isfile(t_):
                os.remove(t_)

@client.on_message(filters.text & filters.user([AUTHOR_ID] + database['author']))
async def start_command(_, m: Message):
    text = str(m.text)
    cmd  = text.lower()
    if cmd == "/help" or cmd == "help":
        await delete(m)
        ret = "**HELP MESSAGE**"
        ret += "\n/Start `Checking bots`\n/Limit `to see max limit recording stream`"
        ret += "\n/Id `Check user id`\n/Groupid `Check group id`"
        ret += "\n/Process `Checking recording on progress.`"
        ret += "\n/Stop [Process ID] `Force stop recording process…`"
        await m.reply(ret)
    elif cmd == "limit" or cmd == "/limit":
        await delete(m)
        await m.reply('Your limit link: %i' % settings['limit'])
    elif cmd.startswith("setlimit") or cmd.startswith("/setlimit") and m.from_user and m.from_user.id in database["author"]:
        cmd = cmd[len("setlimit "):] if cmd.startswith("setlimit") else cmd[len("/setlimit "):]
        if not cmd.isdigit():
            return await m.reply("Link limit must be integers.")
        settings['limit'] = int(cmd)
        return await m.reply(f"Max link limit updated to: {cmd}")
    elif cmd == "id" or cmd == "/id":
        await delete(m)
        user = m.from_user
        if user:
            return await m.reply(f"Your user id: `{user.id}`")
        return await m.reply("Please use your own account, not channel or anonymous.")
    elif cmd == "groupid" or cmd == "/groupid":
        await delete(m)
        chat = m.chat
        if chat and chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
            return await m.reply(m.chat.id)
    elif cmd == "restart" or cmd == "/restart":
        python = sys.executable
        os.execl(python, python, *sys.argv)
    elif cmd == "start" or cmd == "/start":
        await delete(m)
        return await m.reply("Bots active....\n/help to see commands.")
    elif cmd.startswith("/stop"):
        cmd = cmd[len("/stop "):]
        if not cmd.isdigit():
            return await m.reply("Process id must be digits.")
        try:
            os.system(f"kill -9 {cmd}")
        except:
            os.system(f"kill {cmd}")
        return await m.reply('Process has killed, will sent the video shortly.')
    elif cmd.startswith("rtmp") or cmd.startswith("http"):
        url = re.search(r"(\S+)", text).group()
        msg = await m.reply(f"Fetching `url: {url}` **Downloading........**")
        name = f"downloads/{random_name()}.flv"
        result = await run_command("ffmpeg", "-i", url, "-vcodec", "copy", "-acodec", "copy", name, _msg = msg, _url = url, name = name)
        c = ""
        if "wstime" and "wssecret" in text.lower():
            urls = re.findall(r"(\d+_\d+)\?wsSecret=(\w+)\&wsTime=(\d+)", str(m.text))
            if urls and len(urls[0]) == 3:
                urls    = urls[0]
                cl = LiveClient("HONEY")
                uid = urls[0].split("_")[0]
                data = json.loads(cl.getHoneyLiveUser(uid))
                if data.get("code") == 404:
                    c += f"Name: **Unknown**\nID: **{uid}**\nAPP: **BLING²**"
                elif data.get("code") == 200:
                    c += f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **BLING²**"
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
                    c += f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **Sugar Live**"
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
                        c += f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **Mango Live**"
                    else:
                        c += f"Name: **Unknown**\nID: **{uid}**\nAPP: **Mango Live**"
        elif "auth_key" in str(m.text.lower()):
            urls = re.findall(r'(\d+\_\d\S+)', text)
            if urls:
                urls = urls[0]
                url  = f"`rtmp://sea1.live.fantasylive.cc/dreamlive/{urls}`"
                user_id = url.split("/dreamlive/")[1].split("_")[0]
                cl = LiveClient("Dream Live")
                data = json.loads(cl.getDatabaseLiveUser(user_id, 'Dream Live'))
                name, uid = data.get('name', "Unknown"), user_id
                c += f"Name: **{data.get('name')}**\nID: **{uid}**\nAPP: **Dream Live**"
        if isinstance(result, tuple):
            filename, result_ = result[0], result[1]
            if filename and os.path.isfile(filename):
                video = await run_command("ffmpeg", "-i", filename, "-codec", "copy", "-y", filename.replace('.flv', '.mp4'))
                await msg.delete()
                name  = filename.replace(".flv", "")
                if os.path.isfile(filename):
                    os.remove(filename)
                video = ffmpeg.probe(f"{name}.mp4")
                if video.get('format'):
                    dur, size = video["format"].get("duration", 0), video["format"].get("size", 0)
                else:
                    dur, size = 600, 300
                end, duration = 3600, int(float(dur))
                videos = []
                for i in range(0, duration, end):
                    ffmpeg_extract_subclip(f"{name}.mp4", i, end, f"{name}_{i}.mp4")
                    videos.append(f'{name}_{i}.mp4')
                    i += end
                    end += 3600
                    if end > duration:
                        erm = end - duration
                        end = end - erm
                start = datetime.now(timezone("Asia/Jakarta"))
                caption = f"{c}\n{watermark}\n{start.strftime('%d %b %Y')}"
                thums = []
                for no, path in enumerate(videos, start = 1):
                    vid = ffmpeg.probe(path)
                    dur = int(float(vid['format']['duration']))
                    thumb = await run_command("ffmpeg", "-i", path, "-vframes", "1", "-an", "-ss", "00", "-y", path.replace(".mp4", ".png"))
                    thums.append(path.replace(".mp4", ".png"))
                    mm = await msg.reply_video(path, True, caption = caption, duration = dur, width = int(float(vid["streams"][0]["width"])), height = int(vid["streams"][0]["height"]), thumb = path.replace('.mp4', '.png'))
                    try:msss = await _.send_video(database['author'][0], path, caption, duration = dur, thumb = path.replace('.mp4', '.png'))
                    except:msss = None
                    #ry:await _.send_video(database['author'][1], path, caption, duration = dur, thumb = path.replace('.mp4', '.png'))
                    #xcept:pass
                    print(msss)
                    os.remove(path)
                if os.path.isfile(f"{name}.mp4"):os.remove(f"{name}.mp4")
                for t_ in thums:
                    if os.path.isfile(t_):
                        os.remove(t_)
        if url in settings['url']:
            del settings['url'][url]
    elif cmd == "process" or cmd == "/process":
        data = settings["url"].data
        if not data:
            return await m.reply("No process found..")
        ps    = await run_command("pgrep", "-a", "ffmpeg")
        ret   = "Here the process:\n"
        no    = 0
        prces = ps[1].split("\n")
        if not prces[0]:
            settings["url"] = {}
            return await m.reply("`No process found..`")
        urls = [[url.split(' ')[0], url.split(' ')[3]] for url in prces if url.split(' ')[3] in settings['url']]
        if not urls:
            settings["url"] = {}
            return await m.reply("No process found...")
        for pid, url in urls:
            no  += 1
            ret += f"**{no}. {url}** (PID: `{pid}`)\n\n"
        ret += "\n\n/stop [PID]"
        return await m.reply(ret)

async def run():
    await client.start()
    await idle()

if __name__ == "__main__":
    loop.run_until_complete(run())
