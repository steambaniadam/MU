################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV
 
 EH KONTOL BAJINGAN !! KALO MO PAKE DIKODE PAKE AJA BANGSAT!! GAUSAH APUS KREDIT NGENTOT
"""
################################################################

import requests

from Mix import *

__modles__ = "Morse"
__help__ = """
 Morse

• Perintah: `{0}emorse` [teks/balas pesan teks]
• Penjelasan: Untuk meng-encode teks menjadi sandi morse.

• Perintah: `{0}dmorse` [teks/balas pesan teks]
• Penjelasan: Untuk men-decode sandi morse.
"""


@ky.ubot("emorse|dmorse")
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    kimi = c.get_text(m)
    pros = await m.reply(cgr("proses").format(em.proses))
    if m.command[0] == "emorse":

        uri = f"https://api.safone.dev/morse/encode?text={kimi}"
        pot = requests.get(url)
        if pot.status_code == 200:
            res = pot.json()
            await m.reply(f"{em.sukses} Encode Morse\n\n{res}")
        else:
            await m.reply(f"Error: {pot.status_code}")
    elif m.command[0] == "dmorse":
        uri = f"https://api.safone.dev/morse/decode?text={kimi}"
        pot = requests.get(url)
        if pot.status_code == 200:
            res = pot.json()
            await m.reply(f"{em.sukses} Decode Morse\n\n{res}")
        else:
            await m.reply(f"Error: {pot.status_code}")
    else:
        await m.reply(
            f"{em.gagal} Perintah yang anda gunakan salah!! Silahkan lihat bantuan."
        )
    await pros.delete()
    return
