import json
import mimetypes
import re
import urllib.request

import requests
from bs4 import BeautifulSoup
from pyrogram import *

from Mix import *

__modles__ = "Pinterest"
__help__ = "Pinterest"


async def getJson(html):
    soup = BeautifulSoup(html, "html.parser")

    scriptTag = soup.find("script", {"id": "__PWS_DATA__", "type": "application/json"})

    return json.loads(re.findall(r">(.*)<", str(scriptTag))[0])


async def getHtml(url):
    if "pin.it" in url:
        url = requests.get(url).url

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        img_tag = soup.find("img", class_="hCL kVc L4E MIw")
        if img_tag:
            img_url = img_tag.get("currentSrc")
            return img_url, response.text
        else:
            return None, None
    except Exception as e:
        print(e)
        return None, None


async def decideType(jsonData):
    response = jsonData["props"]["initialReduxState"]["pins"]

    if not bool(response):
        return None, None

    _id = [*response.keys()][0]
    data = response[_id]

    if data["videos"]:
        return 0, data["videos"]["video_list"]["V_720P"]["url"]

    if data["embed"]:
        return 1, data["embed"]["src"]

    return 2, data["images"]["orig"]["url"]


@ky.ubot("pint", sudo=True)
async def _(c: nlx, m):
    try:
        url = m.text.split(maxsplit=1)[1]
        MEDIA_URL, HTML = await getHtml(url)

        if MEDIA_URL is None:
            await m.reply_text(
                "[ERROR] Tidak ada gambar yang ditemukan di URL Pinterest"
            )
            return

        JSON = await getJson(HTML)
        TYPE, MEDIA_URL = await decideType(JSON)

        if TYPE is None:
            await m.reply_text("[404] Tidak Ada yang Ditemukan!")
            return

        content_type, _ = mimetypes.guess_type(MEDIA_URL)
        file_extension = mimetypes.guess_extension(content_type)

        if file_extension is None:
            await m.reply_text("Tidak dapat menentukan ekstensi file yang sesuai.")
            return

        file_name = f"{MEDIA_URL.split('/')[-1].split('.')[0]}{file_extension}"
        file_path = f"Pypin/{file_name}"

        reporthook_called = False

        async def reporthook(blocknum, blocksize, totalsize):
            nonlocal reporthook_called
            if not reporthook_called:
                reporthook_called = True
                await c.send_message(m.chat.id, "Sedang mengunduh...")

            readsofar = blocknum * blocksize
            if readsofar > totalsize:
                readsofar = totalsize
            percent = int((readsofar * 50 / totalsize))
            r_size = totalsize / 1024**2
            d_size = readsofar / 1024**2
            pgbar = "[{}{}] ".format(
                "█" * percent, " " * (50 - percent)
            ) + "[{0:.2f}/{1:.2f} MB]".format(d_size, r_size)
            await c.send_message(m.chat.id, f">>>> {pgbar}")

        opener = urllib.request.URLopener()
        opener.addheader("User-Agent", "Mozilla/5.0")
        await opener.retrieve(MEDIA_URL, filename=file_path, reporthook=reporthook)

        await m.reply_document(document=file_path)
    except Exception as e:
        await m.reply_text(f"Terjadi kesalahan: {str(e)}")
