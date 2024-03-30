import requests

from Mix import *

__modles__ = "Proxy"
__help__ = get_cgr("help_prox")


async def fetch_proxies(proxy_type):
    em = Emojik()
    em.initialize()
    url = f"https://www.proxy-list.download/api/v1/get?type={proxy_type}"
    response = requests.get(url)
    if response.status_code == 200:
        proxies = response.text.split("\n")
        proxies.sort()
        formatted_proxies = []
        for i, proxy in enumerate(proxies):
            if proxy.strip():
                formatted_proxies.append(cgr("prox_1").format(proxy))

        if not formatted_proxies:
            formatted_proxies.append(cgr("prox_2").format(em.gagal))

        return formatted_proxies[:10]
    else:
        return None


async def send_proxy(c: nlx, chat_id, proxy_type, proxies):
    em = Emojik()
    em.initialize()
    if proxies:
        teks = cgr("prox_3").format(em.sukses, proxy_type)
        teks += "\n".join(proxies)
        await c.send_message(chat_id, teks)
    else:
        await c.send_message(chat_id, (cgr("prox_4").format(em.gagal)))


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
                (cgr("prox_5").format(em.gagal, m.texy)),
            )
            return

        proxy_type = command
        proxies = await fetch_proxies(proxy_type)
        await send_proxy(c, m.chat.id, proxy_type, proxies)
        await pros.delete()
    except IndexError:
        await c.send_message(
            m.chat.id,
            (cgr("prox_6").format(em.gagal, m.text)),
        )
        await pros.delete()
