
import requests
from pyquery import PyQuery as pq
from pyrogram import *

from Mix import *

__modles__ = "Pinterest"
__help__ = "Pinterest"


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


async def download_file(url, file_path, chat_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(file_path, mode="wb")
                await f.write(await resp.read())
                await f.close()
                await bot.send_message(chat_id, "Download selesai.")


@ky.ubot("pint", sudo=True)
async def _(c: nlx, m):
    try:
        url = m.text.split(maxsplit=1)[1]
        download_url = await get_download_url(url)

        if download_url is None:
            await m.reply_text(
                "[ERROR] Tidak ada gambar atau video yang ditemukan di URL Pinterest"
            )
            return

        if ".mp4" in download_url:
            file_extension = ".mp4"
        else:
            file_extension = ".jpg"

        file_name = f"pinterest_content{file_extension}"
        file_path = f"Pypin/{file_name}"

        await download_file(download_url, file_path, m.chat.id)

        await m.reply_document(document=file_path)
    except Exception as e:
        await m.reply_text(f"Terjadi kesalahan: {str(e)}")
