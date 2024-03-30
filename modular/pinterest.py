import os

import aiofiles
import aiohttp
import requests
from pyquery import PyQuery as pq
from pyrogram import *

from Mix import *

__modles__ = "Pinterest"
__help__ = get_cgr("help_pint")


async def get_download_url(link):
    post_request = requests.post(
        "https://www.expertsphp.com/download.php", data={"url": link}
    )
    request_content = post_request.content
    str_request_content = str(request_content, "utf-8")
    download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")(
        "a"
    ).attr("href")
    return download_url


async def download_file(
    url, file_path, chat_id, caption=None
):  # Tambahkan argumen caption
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(file_path, mode="wb")
                await f.write(await resp.read())
                await f.close()
                if file_path.endswith(".mp4"):
                    await bot.send_video(TAG_LOG, file_path, caption=caption)
                else:
                    await bot.send_photo(TAG_LOG, file_path, caption=caption)
                os.remove(file_path)


@ky.ubot("pint", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    gue = c.me.first_name
    try:
        url = m.text.split(maxsplit=1)[1]
        download_url = await get_download_url(url)

        if download_url is None:
            await m.reply(cgr("pint_1").format(em.gagal))
            await pros.delete()
            return

        if ".mp4" in download_url:
            file_extension = ".mp4"
        else:
            file_extension = ".jpg"

        file_name = f"Pinterest{file_extension}"
        file_path = f"Pypin/{file_name}"

        if not os.path.exists("Pypin"):
            os.makedirs("Pypin")

        await download_file(
            download_url,
            file_path,
            m.chat.id,
            caption=cgr("pint_2").format(em.sukses, gue),
        )

        await m.reply_document(document=file_path)
        await pros.delete()
    except Exception as e:
        await m.reply(f"Error: {str(e)}")
        await pros.delete()
