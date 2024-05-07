import asyncio
import random

from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "Fake Action"
__help__ = "Fake Action"


@ky.ubot("giben", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    await asyncio.sleep(3)
    try:
        if len(m.command) > 1:
            pengguna = m.command[1]
            success_count = random.randint(50, 200)
            failure_count = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Banned :</b>\n\n"
                f"{em.profil} <b>Pengguna : {pengguna}</b>\n"
                f"{em.sukses} <b>Sukses : `{success_count}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{failure_count}` grup.</b>"
            )
            if len(m.command) > 2:
                reason = " ".join(m.command[2:])
                report_message += f"\n\n<b>Alasan : `{reason}`</b>"
            await pros.edit(report_message)
        else:
            await pros.edit("Mohon berikan username atau user ID sebagai argumen.")
    except Exception as e:
        await pros.edit(f"{em.gagal} Gagal membuat laporan Global Banned: {str(e)}")
