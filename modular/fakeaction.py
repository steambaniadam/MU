import asyncio
import random

from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "Fake Action"
__help__ = "Fake Action"


@ky.ubot("giben|gben", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    await asyncio.sleep(3)
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Banned :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n\n<b>{em.block} Alasan : `{alasan}`</b>"
            await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Banned :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{gagal}` grup.</b>"
            )
            await pros.edit(report_message)
    except Exception as e:
        await pros.edit(f"{em.gagal} Gagal membuat laporan Global Banned: {str(e)}")


@ky.ubot("gimute|gmut", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    await asyncio.sleep(3)
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Mute :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n\n<b>{em.block} Alasan : `{alasan}`</b>"
            await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Mute :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{gagal}` grup.</b>"
            )
            await pros.edit(report_message)
    except Exception as e:
        await pros.edit(f"{em.gagal} Gagal membuat laporan Global Mute: {str(e)}")


@ky.ubot("gikick|gkik", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    await asyncio.sleep(3)
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Kick :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{gagal}` grup.</b>"
            )
            if alasan:
                report_message += f"\n\n<b>{em.block} Alasan : `{alasan}`</b>"
            await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            gagal = random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Global Kick :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Sukses : `{sukses}` grup.</b>\n"
                f"{em.gagal} <b>Gagal : `{gagal}` grup.</b>"
            )
            await pros.edit(report_message)
    except Exception as e:
        await pros.edit(f"{em.gagal} Gagal membuat laporan Global Kick: {str(e)}")


@ky.ubot("teep|tf", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    await asyncio.sleep(3)
    try:
        if len(m.command) > 1:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            random.randint(50000, 2000000)
            report_message = (
                f"{em.warn} <b>Laporan Transfer :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Nominal : `Rp.{sukses}`</b>\n"
            )
            if alasan:
                report_message += f"\n\n<b>{em.block} Alasan : `{alasan}`</b>"
            await pros.edit(report_message)
        else:
            pengguna, alasan = await c.extract_user_and_reason(m)
            mention = (await c.get_users(pengguna)).mention
            sukses = random.randint(50, 200)
            random.randint(1, 20)
            report_message = (
                f"{em.warn} <b>Laporan Transfer :</b>\n\n"
                f"{em.profil} <b>Pengguna : {mention}</b>\n"
                f"{em.sukses} <b>Nominal : Rp.`{sukses}`</b>\n"
            )
            await pros.edit(report_message)
    except Exception as e:
        await pros.edit(f"{em.gagal} Gagal membuat laporan Transfer: {str(e)}")
