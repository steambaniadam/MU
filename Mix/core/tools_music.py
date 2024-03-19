# part of https://github.com/thehamkercat/Telegram_VC_Bot

import asyncio
import os
from random import randint
from time import time
from typing import Optional

import pytgcalls
from pyrogram.errors import *
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, EditGroupCallTitle
from pyrogram.raw.types import InputPeerChannel, InputPeerChat
from pytgcalls.exceptions import GroupCallNotFoundError
from youtubesearchpython import VideosSearch

from Mix import *

ACTIVE_CALLS = []
VC_QUEUE = {}
MSGID_CACHE = {}
VIDEO_ON = {}
CLIENTS = {}
CLIENT_TYPE = pytgcalls.GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM
OUTGOING_AUDIO_BITRATE_KBIT = 512
PLAYOUT_FILE = "input.raw"
from .waktu import time_formatter


async def get_group_call(client: nlx, message, err_msg: str = "") -> Optional:
    chat_peer = await client.resolve_peer(message.chat.id)
    if chat_peer:
        full_chat = None
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (await client.send(GetFullChannel(channel=chat_peer))).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.send(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat:
            return full_chat.call
    await message.reply_text(err_msg)
    return None


class MP:
    def __init__(self, chat, video=False):
        self._chat = chat
        self._video = video
        if CLIENTS.get(chat):
            self.group_call = CLIENTS[chat]
        else:
            _client = pytgcalls.GroupCallFactory(
                nlx, CLIENT_TYPE, OUTGOING_AUDIO_BITRATE_KBIT
            )
            _client.enable_logs_to_console = False
            self.group_call = _client.get_group_call()
            CLIENTS.update({chat: self.group_call})

    async def make_vc_active(self):
        if not (
            group_call := (
                await get_group_call(nlx, self._chat, err_msg=", Kesalahan...")
            )
        ):
            return
        try:
            await self.invoke(
                CreateGroupCall(
                    peer=(await self.resolve_peer(self._chat)),
                    random_id=randint(10000, 999999999),
                )
            )
            await nlx.invoke(
                EditGroupCallTitle(call=group_call, title="🎧 Mix Music 🎶")
            )
        except Exception as e:
            LOGGER.error(e)
            return False, e
        return True, None

    async def startCall(self):
        if VIDEO_ON:
            for chats in VIDEO_ON:
                await VIDEO_ON[chats].stop()
            VIDEO_ON.clear()
            await asyncio.sleep(3)
        if self._video:
            for chats in list(CLIENTS):
                if chats != self._chat:
                    await CLIENTS[chats].stop()
                    del CLIENTS[chats]
            VIDEO_ON.update({self._chat: self.group_call})
        if self._chat not in ACTIVE_CALLS:
            try:
                self.group_call.on_network_status_changed(self.on_network_changed)
                self.group_call.on_playout_ended(self.playout_ended_handler)
                await self.group_call.join(self._chat)
            except GroupCallNotFoundError as er:
                LOGGER.info(er)
                dn, err = await self.make_vc_active()
                if err:
                    return False, err
            except Exception as e:
                LOGGER.error(e)
                return False, e
        return True, None

    async def on_network_changed(self, call, is_connected):
        chat = self._chat
        if is_connected:
            if chat not in ACTIVE_CALLS:
                ACTIVE_CALLS.append(chat)
        elif chat in ACTIVE_CALLS:
            ACTIVE_CALLS.remove(chat)

    async def playout_ended_handler(self, call, source, mtype):
        if os.path.exists(source):
            os.remove(source)
        await self.play_from_queue()

    async def play_from_queue(self):
        chat_id = self._chat
        if chat_id in VIDEO_ON:
            await self.group_call.stop_video()
            VIDEO_ON.pop(chat_id)
        try:
            song, title, link, thumb, from_user, pos, dur = await get_from_queue(
                chat_id
            )
            try:
                await self.group_call.start_audio(song)
            except ParticipantJoinMissingError:
                await self.vc_joiner()
                await self.group_call.start_audio(song)
            if MSGID_CACHE.get(chat_id):
                await MSGID_CACHE[chat_id].delete()
                del MSGID_CACHE[chat_id]
            text = f"<strong>🎧 Now playing #{pos}: <a href={link}>{title}</a>\n⏰ Duration:</strong> <code>{dur}</code>\n👤 <strong>Requested by:</strong> {from_user}"

            try:
                xx = await self.send_photo(
                    self._chat,
                    photo=thumb,
                    caption=f"<strong>🎧 Now playing #{pos}: <a href={link}>{title}</a>\n⏰ Duration:</strong> <code>{dur}</code>\n👤 <strong>Requested by:</strong> {from_user}",
                    # parse_mode="html",
                )

            except ChatSendMediaForbidden:
                xx = await self.send_message(
                    self._chat, text, disable_web_page_preview=True
                )
            MSGID_CACHE.update({chat_id: xx})
            VC_QUEUE[chat_id].pop(pos)
            if not VC_QUEUE[chat_id]:
                VC_QUEUE.pop(chat_id)

        except (IndexError, KeyError):
            await self.group_call.stop()
            del CLIENTS[self._chat]
            await nlx.send_messages(TAG_LOG, f"• Berhasil meninggalkan: {chat_id}")
        except Exception as er:
            await nlx.send_message(TAG_LOG, f"Error:{er}")

    async def vc_joiner(self):
        chat_id = self._chat
        done, err = await self.startCall()

        if done:
            await nlx.send_message(
                TAG_LOG,
                f"• Joined VC in <code>{chat_id}</code>",
            )

            return True
        await nlx.send_message(
            TAG_LOG,
            f"<strong>ERROR while Joining Vc -</strong> <code>{chat_id}</code> :\n<code>{err}</code>",
        )
        return False


def add_to_queue(chat_id, song, song_name, link, thumb, from_user, duration):
    try:
        n = sorted(list(VC_QUEUE[chat_id].keys()))
        play_at = n[-1] + 1
    except BaseException:
        play_at = 1
    stuff = {
        play_at: {
            "song": song,
            "title": song_name,
            "link": link,
            "thumb": thumb,
            "from_user": from_user,
            "duration": duration,
        }
    }
    if VC_QUEUE.get(chat_id):
        VC_QUEUE[int(chat_id)].update(stuff)
    else:
        VC_QUEUE.update({chat_id: stuff})
    return VC_QUEUE[chat_id]


def list_queue(chat):
    if VC_QUEUE.get(chat):
        txt, n = "", 0
        for x in list(VC_QUEUE[chat].keys())[:18]:
            n += 1
            data = VC_QUEUE[chat][x]
            txt += f'<strong>{n}. <a href={data["link"]}>{data["title"]}</a> :</strong> <i>By: {data["from_user"]}</i>\n'
        txt += "\n\n....."
        return txt


async def get_from_queue(chat_id):
    play_this = list(VC_QUEUE[int(chat_id)].keys())[0]
    info = VC_QUEUE[int(chat_id)][play_this]
    song = info.get("song")
    title = info["title"]
    link = info["link"]
    thumb = info["thumb"]
    from_user = info["from_user"]
    duration = info["duration"]
    if not song:
        song = await get_stream_link(link)
    return song, title, link, thumb, from_user, play_this, duration


# --------------------------------------------------


async def download(query):
    if query.startswith("https://") and "youtube" not in query.lower():
        thumb, duration = None, "Unknown"
        title = link = query
    else:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        link = data["link"]
        title = data["title"]
        duration = data.get("duration") or "♾"
        thumb = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
    dl = await get_stream_link(link)
    return dl, thumb, title, link, duration


async def get_stream_link(ytlink):
    """
    info = YoutubeDL({}).extract_info(url=ytlink, download=False)
    k = ""
    for x in info["formats"]:
        h, w = ([x["height"], x["width"]])
        if h and w:
            if h <= 720 and w <= 1280:
                k = x["url"]
    return k
    """
    stream = await nlx.bash(f'yt-dlp -g -f "best[height<=?720][width<=?1280]" {ytlink}')
    return stream[0]


async def vid_download(query):
    search = VideosSearch(query, limit=1).result()
    data = search["result"][0]
    link = data["link"]
    video = await get_stream_link(link)
    title = data["title"]
    thumb = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
    duration = data.get("duration") or "♾"
    return video, thumb, title, link, duration


async def dl_playlist(chat, from_user, link):
    # untill issue get fix
    # https://github.com/alexmercerind/youtube-search-python/issues/107
    """
    vids = Playlist.getVideos(link)
    try:
        vid1 = vids["videos"][0]
        duration = vid1["duration"] or "♾"
        title = vid1["title"]
        song = await get_stream_link(vid1['link'])
        thumb = f"https://i.ytimg.com/vi/{vid1['id']}/hqdefault.jpg"
        return song[0], thumb, title, vid1["link"], duration
    finally:
        vids = vids["videos"][1:]
        for z in vids:
            duration = z["duration"] or "♾"
            title = z["title"]
            thumb = f"https://i.ytimg.com/vi/{z['id']}/hqdefault.jpg"
            add_to_queue(chat, None, title, z["link"], thumb, from_user, duration)
    """
    links = await get_videos_link(link)
    try:
        search = VideosSearch(links[0], limit=1).result()
        vid1 = search["result"][0]
        duration = vid1.get("duration") or "♾"
        title = vid1["title"]
        song = await get_stream_link(vid1["link"])
        thumb = f"https://i.ytimg.com/vi/{vid1['id']}/hqdefault.jpg"
        return song, thumb, title, vid1["link"], duration
    finally:
        for z in links[1:]:
            try:
                search = VideosSearch(z, limit=1).result()
                vid = search["result"][0]
                duration = vid.get("duration") or "♾"
                title = vid["title"]
                thumb = f"https://i.ytimg.com/vi/{vid['id']}/hqdefault.jpg"
                add_to_queue(chat, None, title, vid["link"], thumb, from_user, duration)
            except Exception as er:
                LOGGER.info(er)


async def file_download(c, m):
    thumb = "https://telegra.ph//file/e1c16e8991137707c461b.jpg"
    file_name = f"{c.me.id}.mp4"
    title = file_name or f"{str(time())}.mp4"
    file = file_name or f"{str(time())}.mp4"
    replied = m.reply_to_message
    dl = await replied.download()
    duration = time_formatter(file * 1000) if file else "🤷‍♂️"
    return dl, thumb, title, replied.link, duration
