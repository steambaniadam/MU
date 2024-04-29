import io
import os
from asyncio import sleep

import requests

from Mix import *

__modles__ = "Waifu"
__help__ = get_cgr("help_waif")


categories = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "kill",
    "kick",
    "happy",
    "wink",
    "poke",
    "dance",
    "cringe",
]

kueri = [
    "ai",
    "ass",
    "boobs",
    "creampie",
    "paizuri",
    "pussy",
    "random",
    "vtuber",
    "ecchi",
    "ficking",
]


async def download_and_send_image(c: nlx, m, image_url, image_content):
    em = Emojik()
    em.initialize()
    image_bytes = io.BytesIO(image_content)
    image_bytes.name = "image.jpg"

    await c.send_photo(
        m.chat.id,
        photo=image_bytes,
        caption=f"{em.sukses} Downloaded by : {c.me.mention}",
    )

    folder_path = "waifu_images"
    os.makedirs(folder_path, exist_ok=True)
    filename = image_url.split("/")[-1]
    filepath = os.path.join(folder_path, filename)

    if os.path.exists(filepath):
        os.remove(filepath)


@ky.ubot("loly", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    await sleep(2)
    if len(m.command) > 1:
        category = m.text.split(maxsplit=1)[1].lower()
    else:
        categories_text = "\n".join(
            [f"{i+0}) <code>{cat}</code>" for i, cat in enumerate(categories, start=1)]
        )
        await pros.edit(cgr("waif_1").format(em.gagal, categories_text))
        return

    api_url = f"https://api.waifu.pics/sfw/{category}"
    response = requests.get(api_url)

    if response.ok:
        image_url = response.json()["url"]
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            await download_and_send_image(c, m, image_url, image_response.content)
            await pros.delete()
        else:
            return await pros.edit(f"{em.gagal} **Gagal mengunduh gambar.**")
    else:
        return await pros.edit(f"{em.gagal} **Gagal mengambil gambar.**")


@ky.ubot("neko", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    await sleep(2)
    if len(m.command) > 1:
        kuer = m.text.split(maxsplit=1)[1].lower()
    else:
        kategori = "\n".join(
            [f"{i+0}) <code>{cat}</code>" for i, cat in enumerate(kueri, start=1)]
        )
        await pros.edit(cgr("waif_1").format(em.gagal, kategori))
        return

    api_url = f"https://nekos.pro/api/{kuer}"
    response = requests.get(api_url)

    if response.ok:
        image_url = response.json()["url"]
        image_response = requests.get(image_url)

        if image_response.status_code == 200:
            await download_and_send_image(c, m, image_url, image_response.content)
        else:
            return await pros.edit(f"{em.gagal} **Gagal mengunduh gambar.**")
    else:
        return await pros.edit(f"{em.gagal} **Gagal mengambil gambar.**")


TAGS = [
    "maid",
    "waifu",
    "marin-kitagawa",
    "mori-calliope",
    "raiden-shogun",
    "oppai",
    "selfies",
    "uniform",
    "kamisato-ayaka",
    "ass",
    "hentai",
    "milf",
    "oral",
    "paizuri",
    "ecchi",
    "ero",
]


@ky.ubot("waifu", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.edit(cgr("proses").format(em.proses))
    await sleep(2)

    if len(m.command) > 1:
        args = m.command[1:]
        if len(args) == 1:
            kuer = args[0].lower()
            kuen = 3
        elif len(args) == 2:
            kuer = args[0].lower()
            kuen = args[1]
        else:
            await pros.edit(f"{em.gagal} Invalid number of arguments.")
            return
    else:
        tag_list = "\n".join(
            [f"{i+1}) <code>{tag}</code>" for i, tag in enumerate(TAGS)]
        )
        await pros.edit(
            f"Usage: `{m.command}` [query] [quantity]\nExample: `{m.command} oppai 3`\nAvailable tags:\n{tag_list}"
        )
        return

    try:
        kuen = int(kuen)
        if kuen <= 0:
            raise ValueError
    except ValueError:
        await pros.edit(f"{em.gagal} Quantity must be a positive integer.")
        return

    api_url = "https://api.waifu.im/search"
    params = {"included_tags": [kuer], "height": ">=2000", "limit": kuen}

    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            images = data.get("images", [])
            if not images:
                raise IndexError("No images found in the response.")

            image_data = images[0]
            image_url = image_data["url"]
            name_anime = image_data["artist"]["name"]
            desc = image_data["tags"][0]["description"]
            aplod = image_data["uploaded_at"]

            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_content = image_response.content
                image_bytes = io.BytesIO(image_content)
                image_bytes.name = "image.jpg"

                caption = (
                    f"{em.sukses} Successfully Downloaded:\n\n"
                    f"Name = {name_anime}\n"
                    f"Description = {desc}\n"
                    f"Uploaded = {aplod}\n"
                )

                await c.send_photo(m.chat.id, photo=image_bytes, caption=caption)

                folder_path = "waifu_images"
                os.makedirs(folder_path, exist_ok=True)
                filename = image_url.split("/")[-1]
                filepath = os.path.join(folder_path, filename)

                if os.path.exists(filepath):
                    os.remove(filepath)
        except (KeyError, IndexError) as e:
            await pros.edit(f"{em.gagal} Error: {str(e)}")
    else:
        await pros.edit(f"{em.gagal} Failed to fetch the image.")
