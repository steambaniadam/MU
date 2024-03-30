from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

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
async def send_streaming_links(client, message):
    if len(message.command) > 1:
        anime_id = message.command[1]
        streaming_links = get_streaming_links(anime_id)
        if streaming_links:
            buttons = []
            for link_data in streaming_links:
                name = link_data.get("name", "Unknown")
                url = link_data.get("url", "")
                button = InlineKeyboardButton(name, url=url)
                buttons.append([button])
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_text("Pilih platform streaming:", reply_markup=reply_markup)
        else:
            await message.reply_text("Tidak ada informasi streaming untuk anime tersebut.")
    else:
        await message.reply_text("Format perintah salah. Gunakan /streaming [ID Anime]")