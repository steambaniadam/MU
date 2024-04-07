################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
"""
################################################################

import os
import time
from datetime import timedelta
from time import time

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


CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"


async def download_tiktok_video(c, chat_id, tiktok_link):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        with webdriver.Chrome(
            executable_path=CHROMEDRIVER_PATH, options=options
        ) as driver:
            driver.get("https://musicaldown.com/en")
            input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "link_url"))
            )
            input_element.send_keys(tiktok_link)
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "download"))
            )
            download_button.click()
            time.sleep(5)
            download_url = driver.current_url
            video_file_path = f"downloads/{chat_id}_downloaded_video.mp4"
            response = requests.get(download_url)
            with open(video_file_path, "wb") as video_file:
                video_file.write(response.content)
            await c.send_video(chat_id=chat_id, video=video_file_path)
            clear_directory("downloads")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        await c.send_message(
            chat_id=chat_id, text="Tautan rusak atau video gagal diunggah."
        )


def clear_directory(directory):
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


@ky.ubot("dtik", sudo=False)
async def download_tiktok_command(c: nlx, m: Message):
    em = Emojik()
    em.initialize()
    tiktok_link = m.text.split(maxsplit=1)[1]
    pros = await m.edit(cgr("proses").format(em.proses))

    await download_tiktok_video(c, m.chat.id, tiktok_link)

    await pros.delete()


"""
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
"""


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
