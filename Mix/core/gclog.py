################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || Misskaty
 
 MIKIR GOBLOK, TOLOL, IDIOT, NGENTOT, KONTOL, BAJINGAN
"""
################################################################


from os import execvp
from sys import executable
from sys import version as pyver

import wget
from pyrogram import *
from pyrogram import __version__ as pyrover
from pyrogram.errors import *
from pyrogram.types import ChatPrivileges
from pytgcalls import __version__ as pytgver
from team.nandev.class_handler import TAG_LOG
from team.nandev.class_log import LOGGER
from team.nandev.class_modules import CMD_HELP
from team.nandev.database import ndB

from config import *
from Mix import bot, nlx


async def check_logger():
    if not ndB.get_key("TAG_LOG") and log_channel is None:
        LOGGER.info(f"Creating Grup Log...")
        nama = f"Alter-Userbot Logs"
        des = "Jangan Keluar Dari Grup Log Ini\n\nPowered by: @AlteregoNetwork"
        log_pic = "https://telegra.ph//file/be3ec296133b57581e773.jpg"
        gc = await nlx.create_supergroup(nama, des)
        bhan = wget.download(f"{log_pic}")
        gmbr = {"video": bhan} if bhan.endswith(".mp4") else {"photo": bhan}
        kntl = gc.id
        await nlx.set_chat_photo(kntl, **gmbr)
        await nlx.promote_chat_member(
            kntl,
            bot.me.username,
            privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ),
        )
        ndB.set_key("TAG_LOG", kntl)
        await nlx.send_message(kntl, f"<b>Group Log Berhasil Dibuat.</b>")
        LOGGER.info(f"Group Logger Enable...")
        execvp(executable, [executable, "-m", "Mix"])
    else:
        return


async def getFinish():
    emut = await nlx.get_prefix(nlx.me.id)
    xx = " ".join(emut)
    try:
        await bot.send_message(
            int(TAG_LOG),
            f"""
<b>Userbot Successfully Deploy !!</b>

<b>Modules : {len(CMD_HELP)}</b>
<b>Python : {pyver.split()[0]}</b>
<b>Pyrogram : {pyrover}</b>
<b>Pytgcalls : {pytgver}</b>
<b>Prefixes : {xx}</b>
""",
        )
    except (ChannelInvalid, PeerIdInvalid):
        try:
            await nlx.promote_chat_member(
                int(TAG_LOG),
                bot.me.username,
                privileges=ChatPrivileges(
                    can_change_info=True,
                    can_invite_users=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_chat=True,
                    can_manage_video_chats=True,
                ),
            )
            await bot.send_message(
                int(TAG_LOG),
                f"""
<b>Userbot Successfully Deploy !!</b>

<b>Modules : {len(CMD_HELP)}</b>
<b>Python : {pyver.split()[0]}</b>
<b>Pyrogram : {pyrover}</b>
<b>Pytgcalls : {pytgver}</b>
<b>Prefixes : {xx}</b>
""",
            )
        except:
            ndB.del_key("TAG_LOG")
            execvp(executable, [executable, "-m", "Mix"])
