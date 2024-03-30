from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import re

from Mix import *


__modles__ = "Anime Streaming"
__help__ = "Anime Streaming"


URL_REGEX = re.compile(r"""(?i)\b((?:https?://|www\d{0,3}[.]|
                          [a-z0-9.\-][.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|
                          (\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
                          ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip())


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
            buttons_list = [(link_data["name"], link_data["url"]) for link_data in streaming_links]
            keyboard_markup = create_keyboard(buttons_list)
            await message.reply_text("Pilih platform streaming:", reply_markup=keyboard_markup)
        else:
            await message.reply_text("Tidak ada informasi streaming untuk anime tersebut.")
    else:
        await message.reply_text("Format perintah salah. Gunakan /streaming [ID Anime]")


def create_keyboard(buttons_list):
    keyboard_data = dict()
    for text, data in buttons_list:
        keyboard_data[text] = data

    keyboard = ikb(keyboard_data)
    return keyboard


def ikb(data, row_width=2):
    buttons = []
    for text, data in data.items():
        if is_url(data):
            buttons.append(InlineKeyboardButton(text, url=data))
        else:
            buttons.append(InlineKeyboardButton(text, callback_data=data))
    return InlineKeyboardMarkup([buttons])


def is_url(text):
    return bool(URL_REGEX.match(text))