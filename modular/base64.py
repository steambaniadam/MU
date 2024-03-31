import requests

from Mix import *

__modles__ = "Base64"
__help__ = get_cgr("help_enc")


async def process_message(c: nlx, m, text, decode=False):
    em = Emojik()
    em.initialize()
    if text:
        encoding_type = "base64" if not decode else "base64&decode=true"
        url = f"https://networkcalc.com/api/encoder/{text}?encoding={encoding_type}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not decode and "encoded" in data:
                encoded_text = data["encoded"]
                await m.reply(cgr("enc_1").format(em.sukses, encoded_text))
            elif decode and "decoded" in data:
                decoded_text = data["decoded"]
                await m.reply(cgr("enc_2").format(em.sukses, decoded_text))
            else:
                gagal = f"encode" if not decode else "decode"
                await m.reply(cgr("enc_3").format(em.gagal, gagal))
        else:
            await m.reply(cgr("enc_4").format(em.gagal, response.status_code))
    else:
        await m.reply(cgr("enc_5").format(em.gagal))


@ky.ubot("encode", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
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
    pros = await m.reply(cgr("proses").format(em.proses))
    if m.reply_to_message and m.reply_to_message.text:
        text = m.reply_to_message.text
    else:
        text = " ".join(m.command[1:])
    await process_message(c, m, text, decode=True)
    await pros.delete()
