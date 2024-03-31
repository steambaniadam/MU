import requests
import pyrogram
from pyrogram import filters

from Mix import *

__modles__ = "Encoder"
__help__ = "Encoder"

async def send_encoded_message(chat_id, encoded_text):
    await nlx.send_message(chat_id, encoded_text)


async def process_message(c: nlx, m, text):
    url = "https://networkcalc.com/api/encoder/{}!?encoding=base64".format(text)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            encoded_text = data["encoded"]
            await send_encoded_message(m.chat.id, encoded_text)
        else:
            await c.send_message(m.chat.id, "Response status is not OK")
    else:
        await c.send_message(m.chat.id, "Failed to fetch data: {}".format(response.status_code))


@ky.ubot("encode", sudo=True)
async def _(c: nlx, m):
    text = " ".join(m.command[1:])
    await process_message(c, m, text)
