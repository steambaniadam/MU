import requests

from Mix import *

__modles__ = "Encoder"
__help__ = "Encoder"


async def process_message(c: nlx, m, text, decode=False):
    em = Emojik()
    em.initialize()
    encoding_type = "base64" if not decode else "base64&decode=true"
    url = f"https://networkcalc.com/api/encoder/{text}?encoding={encoding_type}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            encoded_text = data["encoded"]
            await m.reply(encoded_text)
        else:
            await c.send_message(m.chat.id, f"{em.gagal}Response status is not OK")
    else:
        await c.send_message(
            m.chat.id,
            "{} Failed to fetch data: {}".format(em.gagal, response.status_code),
        )


@ky.ubot("encode", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = m.reply(cgr("proses").format(em.proses))
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    else:
        text = " ".join(m.command[1:])
    await process_message(c, m, text)
    await pros.delete()


@ky.ubot("decode", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = m.reply(cgr("proses").format(em.proses))
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    else:
        text = " ".join(m.command[1:])
    await process_message(c, m, text, decode=True)
    await pros.delete()
