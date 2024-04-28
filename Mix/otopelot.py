################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Kalo Pake Ini Kode Minimal Cantumkan Credits . Gw Boleh Mikir Juga Anjing, Meski Liat Ultroid
"""
################################################################

import asyncio
import random
import re
from os import execvp
from random import randint
from sys import executable

import wget
from pyrogram.raw.functions.messages import DeleteHistory
from team.nandev.class_log import LOGGER
from team.nandev.database import ndB

from Mix import nlx


def extract_api_token(text):
    match = re.search(r"Use this token to access the HTTP API:\s*([\w:]+)", text)
    if match:
        return match.group(1)
    else:
        return None


def extract_api_token2(text):
    match = re.search(r"Use this token to access the HTTP API:\s*([\w:]+)", text)
    if match:
        return match.group(1)
    else:
        return None


async def autobot():
    LOGGER.info("MEMBUAT BOT TELEGRAM UNTUK ANDA DI @BotFather, Mohon Tunggu")
    gw = nlx.me
    name = gw.first_name + " Asisstant"
    if gw.username:
        username = gw.username + "_bot"
    else:
        username = "mix_" + (str(gw.id))[5:] + "_bot"
    bf = "@BotFather"
    info = await nlx.resolve_peer(bf)
    await nlx.invoke(DeleteHistory(peer=info, max_id=0, revoke=False))
    await nlx.unblock_user(bf)
    await nlx.send_message(bf, "/start")
    await asyncio.sleep(1)
    await nlx.send_message(bf, "/newbot")
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, "Alright, a new bot.", limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone is None or "Sorry, you can't add more than 20 bots." in isdone:
        LOGGER.error(
            "Tolong buat Bot dari @BotFather dan tambahkan tokennya di bot_token, sebagai env var dan mulai ulang saya."
        )
        await nlx.send_message(bf, "/token")
        await asyncio.sleep(1)
        await nlx.send_message(bf, f"@{username}")
        async for msg in nlx.search_messages(
            bf, query="You can use this token to access HTTP API:", limit=1
        ):
            if msg.text:
                bb = msg.text
                token2 = extract_api_token2(bb)
                if token2:
                    ndB.set_key("BOT_TOKEN", token2)
                    LOGGER.info(
                        f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
                    )
                    return await enable_inline(username)
        # import sys
        # sys.exit(1)
    await nlx.send_message(bf, name)
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Good."):
        await nlx.send_message(bf, username)
    await asyncio.sleep(1)
    async for aa in nlx.search_messages(bf, limit=1):
        isdone = aa.text
        break
    else:
        isdone = None
    if isdone.startswith("Sorry,"):
        ran = randint(1, 100)
        username = "mix_" + (str(gw.id))[6:] + str(ran) + "_bot"
        await nlx.send_message(bf, username)
    await asyncio.sleep(3)
    async for aa in nlx.search_messages(
        bf, query="Use this token to access the HTTP API:", limit=1
    ):
        if aa.text:
            donee = aa.text
            token = extract_api_token(donee)
            if token:
                ndB.set_key("BOT_TOKEN", token)
                LOGGER.info(
                    f"Selesai. Berhasil membuat @{username} untuk digunakan sebagai bot asisten Anda!"
                )
                await enable_inline(username)
            else:
                LOGGER.error("Token API tidak ditemukan.")
                import sys

                sys.exit(1)
        else:
            LOGGER.error(
                "Harap Hapus Beberapa bot Telegram Anda di @Botfather atau Setel Var BOT_TOKEN dengan token bot"
            )
            import sys

            sys.exit(1)


async def enable_inline(username):
    gw = nlx.me
    if gw.username:
        user_name = gw.username
    else:
        user_name = gw.mention
    pp = random.choice(
        [
            "https://telegra.ph//file/19b336da463a05d7d8f8c.jpg",
            "https://telegra.ph//file/2eaf853d09c319465a8f4.jpg",
            "https://telegra.ph//file/7d2e8f0ae636e2f6dc381.jpg",
        ]
    )
    bb = wget.download(pp)
    LOGGER.info(f"Menyesuaikan Bot Asisten di @BotFather")
    bf = "BotFather"
    await nlx.send_message(bf, "/setuserpic")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_photo(bf, bb)
    await asyncio.sleep(1)
    await nlx.send_message(bf, "/setabouttext")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"Mix-Userbot Asisten My Owner : @{user_name}")
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setdescription")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_message(
        bf,
        f"Powerful Mix-Userbot Assistant\nMy Owner : @{user_name}\n\nPowered By ~ @KynanSupport",
    )
    await asyncio.sleep(2)
    await nlx.send_message(bf, "/setinline")
    await asyncio.sleep(1)
    await nlx.send_message(bf, f"@{username}")
    await asyncio.sleep(1)
    await nlx.send_message(bf, "Search")
    LOGGER.info("Customisation Done")
    execvp(executable, [executable, "-m", "Mix"])
