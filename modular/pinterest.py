import os
import aiofiles
import aiohttp
import requests
from pyquery import PyQuery as pq
from pyrogram import *
from subprocess import Popen, PIPE

from Mix import *

__modles__ = "Pinterest"
__help__ = get_cgr("help_pint")

async def get_download_url_and_download(link, chat_id, caption=None):
    em = Emojik()
    em.initialize()
    try:
        post_request = requests.post(
            "https://www.expertsphp.com/download.php", data={"url": link}
        )
        request_content = post_request.content
        str_request_content = str(request_content, "utf-8")
        download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")(
            "a"
        ).attr("href")

        if download_url is None:
            await nlx.send_message(chat_id, cgr("pint_3").format(em.gagal, link))
            return

        if ".m3u8" in download_url:
            await convert_m3u8_to_mp4(download_url, "temp.mp4")
            file_path = "temp.mp4"
        else:
            file_extension = ".jpg" if ".jpg" in download_url else ".mp4"
            file_path = f"pinterest_content{file_extension}"

            async with aiohttp.ClientSession() as session:
                async with session.get(download_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(file_path, mode="wb") as f:
                            await f.write(await resp.read())

        if caption:
            await nlx.send_photo(chat_id, file_path, caption=caption)
        else:
            await nlx.send_video(chat_id, file_path, caption=caption)

        os.remove(file_path)

    except Exception as e:
        await nlx.send_message(chat_id, cgr("pint_4").format(em.gagal, str(e)))


async def convert_to_mp4(input_path, output_path):
    command = ['ffmpeg', '-i', input_path, '-c', 'copy', output_path]
    process = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print("Error:", stderr.decode())

async def convert_m3u8_to_mp4(m3u8_link, mp4_output_path):
    response = requests.get(m3u8_link)
    with open('temp.ts', 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    await convert_to_mp4('temp.ts', mp4_output_path)
    os.remove('temp.ts')


@ky.ubot("pint", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    gue = c.me.mention
    try:
        url = m.text.split(maxsplit=1)[1]
        await get_download_url_and_download(
            url, m.chat.id, caption=cgr("pint_2").format(em.sukses, gue)
        )
        await pros.delete()
    except Exception as e:
        await m.reply(cgr("err").format(em.gagal, str(e)))
        await pros.delete()
