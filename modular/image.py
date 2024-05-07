################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################

import os
from io import BytesIO

import requests
from pyrogram.types import InputMediaPhoto

from Mix import *

__models__ = "Image"
__help__ = get_cgr("help_img")


async def search_images(query, max_results=5):
    url = "https://google-api31.p.rapidapi.com/imagesearch"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "google-api31.p.rapidapi.com",
    }
    payload = {
        "text": query,
        "safesearch": "off",
        "region": "wt-wt",
        "color": "",
        "size": "",
        "type_image": "",
        "layout": "",
        "max_results": max_results,
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching images: {e}")
        return None


@ky.ubot("image|img", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        query = ""
        max_results = 1
        if len(m.command) >= 2:
            query = m.text.split(None, 1)[1]
            if len(m.command) >= 3:
                max_results = int(m.command[2])
        elif m.reply_to_message:
            query = m.reply_to_message.text
            if len(m.command) == 2:
                max_results = int(m.command[1])

        await m.reply(cgr("proses").format(em.proses))
        result = await search_images(query, max_results)
        img_res = result.get("result", [])
        for img_inf in img_res:
            image_url = img_inf.get("image")
            if image_url and image_url.startswith("http"):
                response = requests.get(image_url)
                if response.status_code == 200:
                    img = BytesIO(response.content)
                    media = InputMediaPhoto(img)
                    await m.reply_media_group(
                        [media], reply_to_message_id=ReplyCheck(m)
                    )
                    try:
                        os.remove(media)
                    except:
                        pass
                else:
                    continue
    except Exception as e:
        print(f"Error: {e}")
        return


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
