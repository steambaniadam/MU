import urllib.parse

import requests
from bs4 import BeautifulSoup
from pyrogram.types import Message

from Mix import *

__module__ = "Google"
__help__ = "Google"


def google_search(query, limit=3):
    encoded_query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all("div", class_="tF2Cxc")
        results = []
        for result in search_results[:limit]:
            title = result.find("h3", class_="LC20lb DKV0Md").text
            link = result.find("a")["href"]
            results.append({"title": title, "link": link})
        return results
    else:
        print("Failed to perform Google search")
        return []


@ky.ubot("google", sudo=True)
async def google_command(c: nlx, m: Message):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    query = m.text.split(maxsplit=1)[1]
    results = google_search(query)
    if results:
        response = f"{em.sukses} **Pertanyaan :** `{query}`\n\n"
        for i, result in enumerate(results, start=1):
            response += f"{i}. [{result['title']}]({result['link']})\n\n"
        await m.reply(response, disable_web_page_preview=True)
        await pros.delete()
    else:
        await m.reply(
            f"{em.gagal} Maaf, tidak dapat menemukan hasil untuk pencarian ini."
        )
        await pros.delete()
