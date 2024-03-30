import requests
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Mix import *

__modles__ = "Anime Video"
__help__ = "Anime Streaming"


def get_streaming_links(anime_id):
    url = f"https://api.jikan.moe/v4/anime/{anime_id}/streaming"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", [])
        return data
    else:
        return []


@ky.ubot("streaming", sudo=True)
async def send_streaming_links(c :nlx, m):
    if len(m.command) > 1:
        anime_id = m.command[1]
        streaming_links = get_streaming_links(anime_id)
        if streaming_links:
            buttons = []
            for link_data in streaming_links:
                name = link_data.get("name", "Unknown")
                url = link_data.get("url", "")
                button = InlineKeyboardButton(name, url=url)
                buttons.append([button])
            reply_markup = InlineKeyboardMarkup(buttons)
            await m.reply(
                "Pilih platform streaming:", reply_markup=reply_markup
            )
        else:
            await m.reply(
                "Tidak ada informasi streaming untuk anime tersebut."
            )
    else:
        await m.reply(f"Format perintah salah. Gunakan `{m.text}` [ID Anime]")
