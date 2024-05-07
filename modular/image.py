################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import os
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from pyrogram.types import InputMediaPhoto
from Mix import *


__models__ = "Image"
__help__ = get_cgr("help_img")



async def search_images(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        image_tags = soup.find_all('img', class_='t0fcAb')
        image_urls = [img['src'] for img in image_tags]
        return image_urls
    except Exception as e:
        print(f"Error fetching images: {e}")
        return []


@ky.ubot("image|img", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    try:
        if len(m.command) < 2 and not rep:
            await m.reply(f"{em.gagal} **MINIMAL KASIH QUERY BWANG!!**")
            return
        pros = await m.reply(cgr("proses").format(em.proses))
        if rep:
            query = rep.text
        else:
            query = m.text.split(None, 1)[1]
        limit = 1
        if len(m.command) == 3:
            limit = int(m.text.split(None, 2)[2])
        images = await search_images(query)
        if images:
            for img_url in images[:limit]:
                await m.reply_photo(img_url)
        else:
            await m.reply(f"{em.gagal} **Gambar tidak ditemukan.**")
    except Exception as e:
        print(f"Error processing image search: {e}")
        await m.reply(f"{em.gagal} **Terjadi kesalahan saat mencari gambar.**")
    finally:
        await pros.delete()


"""
@ky.ubot("imeg", sudo=True)
async def _(c: nlx, m):
    query = m.text.split(1)
    images = search_images(query)
    for image in images:
        print(image)




async def search_image_and_reply(query, m, lim):
    meki = SafoneAPI()
    results = await meki.image(query, lim)
    img_res = results.get("results", [])
    for img_inf in img_res:
        image_url = img_inf.get("imageUrl")
        if image_url and image_url.startswith("http"):
            response = requests.get(image_url)
            if response.status_code == 200:
                img = BytesIO(response.content)
                media = InputMediaPhoto(img)
                await m.reply_media_group([media], reply_to_message_id=ReplyCheck(m))
                try:
                    os.remove(media)
                except:
                    pass
            else:
                continue
        else:
            continue
"""