import requests

from Mix import *

__modles__ = "Proxy"
__help__ = get_cgr("help_prox")


async def fetch_proxies(proxy_type):
    url = f"https://www.proxy-list.download/api/v1/get?type={proxy_type}"
    response = requests.get(url)
    if response.status_code == 200:
        proxies = response.text.split("\n")
        proxies.sort()
        formatted_proxies = []
        for i, proxy in enumerate(proxies, start=1):
            if proxy.strip():
                formatted_proxies.append(f"**{i}) `{proxy}`**")

        if not formatted_proxies:
            formatted_proxies.append("1) No valid proxy found")

        return formatted_proxies[:10]
    else:
        return None


async def send_proxy(c: nlx, chat_id, proxy_type, proxies):
    em = Emojik()
    em.initialize()
    if proxies:
        teks = f"{em.sukses}**Berikut adalah daftar proxy `{proxy_type}` :**\n\n"
        formatted_message = teks + "\n".join(proxies)
        await c.send_message(chat_id, formatted_message)
    else:
        await c.send_message(
            chat_id, f"{em.gagal} Tidak dapat menemukan proxy yang valid."
        )


@ky.ubot("getproxy", sudo=True)
async def get_proxy_command(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        pros = await m.reply(cgr("proses").format(em.proses))
        command = m.text.split()[1].lower()
        if command not in ["http", "socks4", "socks5"]:
            await c.send_message(
                m.chat.id,
                f"{em.gagal} <b>Perintah tidak valid. \nGunakan perintah {m.text} [`http`|`socks4`|`socks5`]</b>",
            )
            return

        proxy_type = command
        proxies = await fetch_proxies(proxy_type)
        await send_proxy(c, m.chat.id, proxy_type, proxies)
        await pros.delete()
    except IndexError:
        await c.send_message(
            m.chat.id,
            f"{em.gagal} <b>Perintah tidak valid.\nGunakan perintah `{m.text}` [`http`|`socks4`|`socks5`]</b>",
        )
        await pros.delete()
