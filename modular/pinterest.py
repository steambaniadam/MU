import os
from subprocess import PIPE, Popen

import requests
from pyrogram import *

from Mix import *

__modles__ = "Pinterest"
__help__ = get_cgr("help_pint")


async def download_m3u8_and_convert_to_mp4(m3u8_link, chat_id, caption=None):
    em = Emojik()
    em.initialize()
    try:
        response = requests.get(m3u8_link)
        with open("temp.m3u8", "wb") as f:
            f.write(response.content)
        await convert_m3u8_to_mp4("temp.m3u8", "temp.mp4")
        if caption:
            await nlx.send_video(chat_id, "temp.mp4", caption=caption)
        else:
            await nlx.send_video(chat_id, "temp.mp4")
        os.remove("temp.m3u8")
        os.remove("temp.mp4")

    except Exception as e:
        await nlx.send_message(chat_id, cgr("pint_4").format(em.gagal, str(e)))


async def convert_m3u8_to_mp4(m3u8_input_path, mp4_output_path):
    command = ["ffmpeg", "-i", m3u8_input_path, "-c", "copy", mp4_output_path]
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print("Error:", stderr.decode())


@ky.ubot("pint", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    gue = c.me.mention
    try:
        url = m.text.split(maxsplit=1)[1]

        if url.endswith((".jpg", ".jpeg", ".png")):
            await nlx.send_photo(m.chat.id, url, caption=caption)
        elif url.endswith(".m3u8"):
            await download_m3u8_and_convert_to_mp4(
                url, m.chat.id, caption=cgr("pint_2").format(em.sukses, gue)
            )
        else:
            await nlx.send_document(m.chat.id, url, caption=caption)

        await pros.delete()
    except Exception as e:
        await m.reply(cgr("err").format(em.gagal, str(e)))
        await pros.delete()
