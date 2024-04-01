import asyncio

import requests
from pyrogram.enums import *
from pyrogram.errors import *
from pyrogram.types import *

from Mix import *

__modules__ = "Cek Spam"
__help__ = "Cek Spam"


filter_active = False


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
    if message.from_user:
        is_spam, result = check_user_in_cas(message.from_user.id)
        if is_spam:
            user_id = message.from_user.id
            message.reply(f"Pengguna ini `{user_id}` terdeteksi melakukan spam.")
            if "offenses" in result:
                for url in result["messages"]:
                    message.reply(f"Spam URL: {url}")
            return True
    return False


@ky.ubot("cekspam", sudo=True)
async def cek_spam(c: nlx, m):
    if len(m.command) > 1:
        user_id = m.command[1]
        is_spam, result = check_user_in_cas(user_id)
        if is_spam:
            message = f"Pengguna `{user_id}` terdeteksi melakukan spam."
            if "offenses" in result:
                message += "\n\nSpam URL:\n"
                for url in result["messages"]:
                    message += f"{url}\n"
            await m.reply(message, disable_web_page_preview=True)

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
                                f"Saya harus membatasi `{user_id}` karena terdeteksi melakukan SPAM!",
                            )
                        except Exception as e:
                            await m.reply(f"Tidak dapat membatasi pengguna: {e}")
            except PeerIdInvalid:
                await m.reply(
                    f"`{user_id}` tidak berada di dalam grup, maka saya mengabaikannya"
                )
            except Exception as e:
                await m.reply(
                    f"Terjadi kesalahan saat mengambil anggota obrolan\nKarena : `{e}`"
                )
        else:
            await m.reply(f"Pengguna `{user_id}` tidak terdeteksi melakukan spam.")
    else:
        await m.reply(
            f"Gunakan perintah `{m.text} [user_id]` untuk melakukan pengecekan spam."
        )


@ky.ubot("checkspam", sudo=True)
async def _(c: nlx, m):
    global filter_active
    chat_member = await c.get_chat_member(m.chat.id, (await c.get_me()).id)
    if chat_member.status in (
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.OWNER,
    ):
        if len(m.command) > 1:
            status = m.command[1].lower()
            if status == "on":
                filter_active = True
                await m.reply("Filter Cek Spam Bot telah diaktifkan.")
            elif status == "off":
                filter_active = False
                await m.reply("Filter Cek Spam Bot telah dinonaktifkan.")
        else:
            await m.reply(
                f"Gunakan perintah `{m.text} on` untuk mengaktifkan filter atau `{m.text} off` untuk menonaktifkannya."
            )
    else:
        await m.reply(
            f"Maaf, Anda tidak memiliki izin untuk menggunakan perintah ini di `{m.chat.id}`."
        )


async def on_message(c: nlx, m):
    if filter_active:
        if c.is_admin(m.chat.id):
            chat_members = await c.get_chat_members(m.chat.id)
            for member in chat_members:
                if check_spam(member):
                    permissions = await c.get_permissions(m.chat.id, c.me.id)
                    if (
                        permissions.can_restrict_members
                        and permissions.can_delete_messages
                    ):
                        try:
                            await c.delete_messages(m.chat.id, m.message_id)
                            await c.restrict_chat_member(
                                m.chat.id,
                                member.user.id,
                                permissions=None,
                                until_date=None,
                            )
                        except FloodWait as e:
                            tunggu = asyncio.sleep(e.value)
                            await m.reply(
                                f"Tunggu `{tunggu} detik` sebelum melanjutkan filter pengguna."
                            )
                        except Exception as e:
                            await m.reply(
                                f"Gagal memute atau menghapus pesan. Error: {e}"
                            )
        else:
            await m.reply(
                f"Maaf, Anda tidak memiliki izin untuk menggunakan perintah ini di `{m.chat.id}`."
            )
