import asyncio

import requests
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from Mix import *

__modules__ = "Cek Spam"
__help__ = "Cek Spam"


filter_active = True


def check_user_in_cas(user_id):
    cas_api_endpoint = f"https://api.cas.chat/check?user_id={user_id}"
    response = requests.get(cas_api_endpoint)
    if response.status_code == 200:
        data = response.json()
        if data.get("ok", False):
            return True, data["result"]
        else:
            return False, None
    else:
        print("Gagal konek ke CAS API")
        return False, None


def check_spam(message):
    em = Emojik()
    em.initialize()
    if message.from_user:
        is_spam, result = check_user_in_cas(message.from_user.id)
        if is_spam:
            user_id = message.from_user.id
            message.reply(f"{em.warn} **Pengguna ini `{user_id}` terdeteksi melakukan spam.**")
            if "offenses" in result:
                for url in result["messages"]:
                    message.reply(f"{em.suksesk} Spam URL: `{url}`")
            return True
    return False


@ky.ubot("cekspam", sudo=True)
async def cek_spam(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) > 1:
        user_id = m.command[1]
        is_spam, result = check_user_in_cas(user_id)
        if is_spam:
            message = f"{em.warn} **Pengguna `{user_id}` terdeteksi melakukan spam.**"
            if "offenses" in result:
                message += f"\n\n{em.sukses} **Spam URL:**\n"
                for url in result["messages"]:
                    message += f"`{url}`\n"
            await pros.edit(message, disable_web_page_preview=True)

            try:
                chat_member = await c.get_chat_member(m.chat.id, (await c.get_me()).id)
                if chat_member.status in (
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.OWNER,
                ):
                    permissions = await c.get_chat_member(m.chat.id, user_id)
                    if permissions.can_restrict_members:
                        try:
                            chat_privileges = ChatPrivileges(
                                can_restrict_members=True, can_delete_messages=True
                            )
                            await c.restrict_chat_member(
                                m.chat.id, user_id, permissions=chat_privileges
                            )
                            await c.send(
                                m.chat.id,
                                f"{em.warn} **Saya harus membatasi `{user_id}` karena terdeteksi melakukan SPAM!**"
                            )
                        except PeerIdInvalid:
                            await pros.edit(
                                f"{em.gagal} `{user_id}` **tidak berada di dalam grup dan saya mengabaikannya**"
                            )
                        except Exception as e:
                            await pros.edit(f"{em.gagal} **Tidak dapat membatasi pengguna:**\n`{e}`")
            except Exception as e:
                await pros.edit(
                    f"**Terjadi kesalahan saat mengambil anggota obrolan\nKarena :** `{e}`"
                )
        else:
            await pros.edit(f"{em.sukses} **Pengguna `{user_id}` tidak terdeteksi melakukan spam.**")
    else:
        await pros.edit(
            f"{em.gagal} **Gunakan perintah `{m.text} [user_id]` untuk melakukan pengecekan spam.**"
        )


@ky.ubot("checkspam", sudo=True)
async def check_spam_status(c: nlx, m):
    global filter_active
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    chat_member = await c.get_chat_member(m.chat.id, m.from_user.id)
    if chat_member.status not in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ):
        await pros.edit(
            f"{em.gagal} Maaf, Anda tidak memiliki izin untuk menggunakan perintah ini di `{m.chat.id}`."
        )
        return

    if len(m.command) > 1:
        status = m.command[1].lower()
        if status == "on":
            if filter_active:
                await pros.edit(f"{em.gagal} **Filter Spam Bot sudah aktif.**")
            else:
                filter_active = True
                await pros.edit(f"{em.sukses} **Berhasil mengaktifkan Filter Spam Bot.**")
        elif status == "off":
            if not filter_active:
                await pros.edit(f"{em.gaga} **Saat ini memang belum mengaktifkan Filter Spam Bot.**")
            else:
                filter_active = False
                await pros.edit(f"{em.sukses} **Filter Spam Bot berhasil di Non-Aktifkan.**")
        else:
            await pros.edit(
                f"{em.gagal} **Gunakan `{m.text} on` untuk mengaktifkan atau `{m.text} off` untuk menonaktifkan Filter Spam Bot.**"
            )
    else:
        await pros.edit(
            f"{em.gagal} **Gunakan perintah `{m.text} [on/off]` untuk mengaktifkan atau menonaktifkan Filter Spam Bot.**"
        )


async def on_message(c: nlx, m):
    em = Emojik()
    em.initialize()
    if filter_active:
        if m.from_user:
            user_id = m.from_user.id
            is_admin = (await c.get_chat_member(m.chat.id, c.get_me().id)).status in (
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            )
            if is_admin:
                chat_members = await c.get_chat_members(m.chat.id)
                for member in chat_members:
                    if member.user.id == user_id and check_spam(m):
                        try:
                            permissions = await c.get_chat_member(m.chat.id, user_id)
                            if permissions.can_restrict_members:
                                chat_privileges = ChatPrivileges(
                                    can_restrict_members=True, can_delete_messages=True
                                )
                                await c.delete_messages(m.chat.id, m.message_id)
                                await c.restrict_chat_member(
                                    m.chat.id,
                                    user_id,
                                    permissions=chat_privileges,
                                    until_date=None,
                                )
                                await c.send_message(m.chat.id,
                                    f"**User `{user_id}` telah dibatasi karena terdeteksi melakukan spam.**"
                                )
                                return
                        except FloodWait as e:
                            tunggu = asyncio.sleep(e.value)
                            await c.send_message(m.chat.id,
                                f"**Tunggu `{tunggu} detik` sebelum melanjutkan filter pengguna.**"
                            )
                            return
                        except Exception as e:
                            await c.send_message(m.chat.id, f"**Gagal membatasi pengguna karena :** `{e}`")
                            return
                await c.send_message(m.chat.id, f"`{user_id}` **tidak ditemukan dalam grup.**")
            else:
                await c.send_message(m.chat.id,
                    f"**Maaf, Anda tidak memiliki izin untuk menggunakan perintah ini di : `{m.chat.id}`**."
                )
    else:
        await c.send_message(m.chat.id, "**Filter Cek Spam Bot saat ini tidak aktif.**")
