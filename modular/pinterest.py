import os
import aiofiles
import aiohttp
import requests
from pyquery import PyQuery as pq
from pyrogram import *

from Mix import *

__modles__ = "Pinterest"
__help__ = get_cgr("help_pint")

async def download_file_from_url(url, chat_id, caption=None):
    em = Emojik()
    em.initialize()
    try:
        post_request = requests.post(
            "https://www.expertsphp.com/download.php", data={"url": url}
        )
        request_content = post_request.content
        str_request_content = str(request_content, "utf-8")
        download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")("a").attr("href")

        if download_url is None:
            await nlx.send_message(chat_id, cgr("pint_1").format(em.gagal))
            return

        file_extension = ".mp4" if ".mp4" in download_url else (".jpg" if ".jpg" in download_url else ".m3u8")
        file_name = f"pinterest_content{file_extension}"
        file_path = f"Pypin/{file_name}"

        if not os.path.exists("Pypin"):
            os.makedirs("Pypin")

        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as resp:
                if resp.status == 200:
                    async with aiofiles.open(file_path, mode="wb") as f:
                        await f.write(await resp.read())

                    if file_extension == ".jpg":
                        await nlx.send_photo(chat_id, file_path, caption=caption)
                    elif file_extension == ".mp4":
                        if file_extension == ".m3u8":
                            mp4_path = f"Pypin/pinterest_content.mp4"
                            await convert_m3u8_to_mp4(file_path, mp4_path)
                            await nlx.send_video(chat_id, mp4_path, caption=caption)
                            os.remove(mp4_path)
                        else:
                            await nlx.send_video(chat_id, file_path, caption=caption)
                    else:
                        await nlx.send_document(chat_id, file_path, caption=caption)
                    
                    os.remove(file_path)

    except Exception as e:
        await nlx.send_message(chat_id, f"Error: {str(e)}")


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
    gue = c.me.first_name
    try:
        url = m.text.split(maxsplit=1)[1]
        await download_file_from_url(url, m.chat.id, caption=cgr("pint_2").format(em.sukses, gue))
        await pros.delete()
    except Exception as e:
        await m.reply(cgr("err").format(em.gagal, str(e)))
        await pros.delete()
