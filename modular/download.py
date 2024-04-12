################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os
import subprocess
import time
from datetime import timedelta
from time import time

import requests
import wget
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.file_id import *
from pyrogram.raw.functions.messages import *
from pyrogram.types import *
from youtubesearchpython import VideosSearch

from Mix import Emojik, YoutubeDownload, cgr, get_cgr, ky, nlx, progress

__modles__ = "Download"
__help__ = get_cgr("help_download")


def get_video_dimensions(file_path):
    width, height = 0, 0
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=p=0:s=x",
        file_path,
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        dimensions = result.stdout.decode().split("x")
        if len(dimensions) == 2:
            width, height = map(int, dimensions)
    return width, height


def clear_directory(directory):
    command = ["rm", "-rf", directory]
    subprocess.run(command)


async def download_tiktok_video(c, chat_id, tiktok_link):
    try:
        output_filename = "media/downloaded_video.%(ext)s"

        command = ["yt-dlp", "-o", output_filename, tiktok_link]
        subprocess.check_call(command)

        width, height = get_video_dimensions("media/downloaded_video.mp4")

        with open("media/downloaded_video.mp4", "rb") as video_file:
            await c.send_video(
                chat_id=chat_id,
                video=video_file,
                width=width,
                height=height,
            )

        clear_directory("media")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        await c.send_message(
            chat_id=chat_id, text="Tautan rusak atau video gagal diunggah."
        )


@ky.ubot("dtik", sudo=False)
async def download_tiktok_command(c: nlx, m: Message):
    em = Emojik()
    em.initialize()
    tiktok_link = m.text.split(maxsplit=1)[1]
    pros = await m.edit(cgr("proses").format(em.proses))

    await download_tiktok_video(c, m.chat.id, tiktok_link)

    await pros.delete()


@ky.ubot("vtube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=True)
    except Exception as error:
        return await pros.reply_text(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_video(
        m.chat.id,
        video=file_name,
        thumb=thumbnail,
        file_name=title,
        duration=duration,
        supports_streaming=True,
        caption=data_ytp.format(
            "VIDEO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp4",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


@ky.ubot("stube", sudo=True)
async def _(c, m):
    em = Emojik()
    em.initialize()
    if len(m.command) < 2:
        return await m.reply(cgr("down_1").format(em.gagal, m.command))
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        search = VideosSearch(m.text.split(None, 1)[1], limit=1).result()["result"][0]
        link = f"https://youtu.be/{search['id']}"
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    try:
        (
            file_name,
            title,
            url,
            duration,
            views,
            channel,
            thumb,
            data_ytp,
        ) = await YoutubeDownload(link, as_video=False)
    except Exception as error:
        return await pros.edit(cgr("err").format(em.gagal, error))
    thumbnail = wget.download(thumb)
    await c.send_audio(
        m.chat.id,
        audio=file_name,
        thumb=thumbnail,
        file_name=title,
        performer=channel,
        duration=duration,
        caption=data_ytp.format(
            "AUDIO",
            title,
            timedelta(seconds=duration),
            views,
            channel,
            url,
            c.me.mention,
        ),
        progress=progress,
        progress_args=(
            pros,
            time(),
            cgr("proses").format(em.proses),
            f"{search['id']}.mp3",
        ),
        reply_to_message_id=m.id,
    )
    await pros.delete()
    await m.delete()
    for files in (thumbnail, file_name):
        if files and os.path.exists(files):
            os.remove(files)


async def extract_url_and_media_info(url):
    try:
        tweet_url = "https://twitter-x-media-download.p.rapidapi.com/media"
        payload = {"url": url, "proxy": ""}
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
            "X-RapidAPI-Host": "twitter-x-media-download.p.rapidapi.com",
        }
        response = requests.post(tweet_url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tweet_result = data.get("tweetResult")
            if tweet_result:
                result = tweet_result.get("result")
                if result:
                    media_info = result.get("extended_entities", {}).get("media")
                    if media_info:
                        for media in media_info:
                            media_type = media.get("type")
                            if media_type == "photo":
                                media_url = media.get("media_url_https")
                                content_type = "photo"
                                break
                            elif media_type == "video":
                                variants = media.get("video_info", {}).get(
                                    "variants", []
                                )
                                for variant in variants:
                                    if variant.get("content_type") == "video/mp4":
                                        media_url = variant.get("url")
                                        content_type = "video"
                                        break
                                else:
                                    media_url = None
                                    content_type = None
                                break
                        else:
                            media_url = None
                            content_type = None
                    else:
                        media_url = None
                        content_type = None
                else:
                    media_url = None
                    content_type = None
            else:
                media_url = None
                content_type = None
            return content_type, media_url
        else:
            return None, None
    except (KeyError, IndexError):
        return None, None


async def download_and_send_file(message, url, content_type):
    try:
        file_name = url.split("/")[-1]
        subprocess.run(["wget", url, "-O", file_name])
        if content_type == "photo":
            await message.reply_photo(
                photo=file_name, caption="File yang diunduh dari URL."
            )
        elif content_type == "video":
            await message.reply_video(
                video=file_name, caption="File yang diunduh dari URL."
            )
        else:
            await message.reply_document(
                document=file_name, caption="File yang diunduh dari URL."
            )
        os.remove(file_name)
    except Exception as e:
        await message.reply_text(f"Gagal mengunduh atau mengirim file: {e}")


@ky.ubot("twit", sudo=True)
async def twit_dl(c: nlx, m: Message):
    em = Emojik()
    em.initialize()
    try:
        tweet_url = m.text.split(maxsplit=1)[1]
    except IndexError:
        await m.reply("Silakan berikan URL Twitter.")
        return

    mention = c.me.mention
    pros = await m.edit(cgr("proses").format(em.proses))
    content_type, media_url = await get_media(tweet_url)

    if media_url:
        try:
            file_name = media_url.split("/")[-1]
            subprocess.run(["wget", media_url, "-O", file_name])
            captions = f"{em.sukses} Successfully Downloaded by: {mention}"
            if content_type == "photo":
                await c.send_photo(m.chat.id, photo=file_name, caption=captions)
            elif content_type == "video":
                await c.send_video(m.chat.id, video=file_name, caption=captions)
            elif content_type == "raw":
                await c.send_document(m.chat.id, document=file_name, caption=captions)
            os.remove(file_name)
        except Exception as e:
            await m.reply(f"Error: {e}")
    else:
        await m.reply("Failed to get media URL.")
    await pros.delete()


"""
import os

import requests


async def get_media(tweet_url):
    url = "https://twitter-x-media-download.p.rapidapi.com/media"
    payload = {"url": tweet_url}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "twitter-x-media-download.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        tweet_result = data.get("tweetResult")
        if tweet_result:
            result = tweet_result.get("result")
            if result:
                media_info = result.get("extended_entities", {}).get("media")
                if media_info:
                    for media in media_info:
                        media_type = media.get("type")
                        if media_type == "photo":
                            media_url = media.get("media_url_https")
                            content_type = "photo"
                            break
                        elif media_type == "video":
                            variants = media.get("video_info", {}).get("variants", [])
                            for variant in variants:
                                if variant.get("content_type") == "video/mp4":
                                    media_url = variant.get("url")
                                    content_type = "video"
                                    break
                            else:
                                media_url = None
                                content_type = None
                            break
                    else:
                        media_url = None
                        content_type = None
                else:
                    media_url = None
                    content_type = None
            else:
                media_url = None
                content_type = None
        else:
            media_url = None
            content_type = None
        print("Media URL:", media_url)
        return content_type, media_url
    else:
        return None, None


async def download_file(media_url, file_name):
    response = requests.get(media_url)
    if response.status_code == 200:
        with open(file_name, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download media: {response.status_code}")


@ky.ubot("twit", sudo=True)
async def twit_dl(c: nlx, m: Message):
    em = Emojik()
    em.initialize()
    tweet_url = m.text.split(maxsplit=1)[1]
    mention = c.me.mention
    pros = await m.edit(cgr("proses").format(em.proses))
    content_type, media_url = await get_media(tweet_url)
    if media_url:
        try:
            file_extension = media_url.split(".")[-1].lower()
            file_name = f"media_{m.chat.id}.{file_extension}"
            await download_file(media_url, file_name)
            captions = f"{em.sukses} Successfully Downloaded by: {mention}"
            if content_type == "photo":
                await c.send_photo(m.chat.id, photo=file_name, caption=captions)
            elif content_type == "video":
                await c.send_video(m.chat.id, video=file_name, caption=captions)
            elif content_type == "raw":
                await c.send_document(m.chat.id, document=file_name, caption=captions)
            os.remove(file_name)
        except Exception as e:
            await m.reply(f"Error: {e}")
    else:
        await m.reply("Failed to get media URL.")

    await pros.delete()
"""
