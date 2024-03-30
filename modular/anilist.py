"""
import requests
from pyrogram import *

from Mix import *

__modules__ = "Anime List"
__help__ = "Anime List"


@ky.ubot("anilist", sudo=True)
async def anilist_command(c: nlx, m):
    args = m.command
    if len(args) < 2:
        await m.reply("Please provide the ID of the anime.")
        return

    anime_id = args[1]

    url = f"https://api.jikan.moe/v4/anime/{anime_id}/videos"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data and "promo" in data:
            promos = data["promo"]
            for promo in promos:
                title = promo["title"]
                youtube_id = promo["trailer"]["youtube_id"]
                message_text = f"Title: {title}\nYouTube ID: {youtube_id}"
                await m.reply(message_text, reply_to_message_id=ReplyCheck(m))
        else:
            await m.reply("No promo videos found for this anime.")
    else:
        await m.reply(
            f"Failed to fetch data. Status code: {response.status_code}",
            reply_to_message_id=ReplyCheck(m),
        )
"""

import requests
from bs4 import BeautifulSoup
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Mix import *

__modles__ = "Anime Movie"
__help__ = "Anime Movie"


def get_streaming_link(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    player_options = soup.find_all("div", class_="east_player_option")
    streaming_links = {}
    for option in player_options:
        option_name = option.span.text.strip()
        link = option["data-post"]
        streaming_links[option_name] = link
    return streaming_links


@ky.ubot("anilist")
async def anilist_command(c: nlx, m):
    if len(m.command) < 2:
        await m.reply_text(f"Silakan masukkan judul anime setelah perintah `{m.text}` [judul anime]")
        return

    anime_title = "-".join(m.command[1:])
    url = f"https://samehadaku.email/{anime_title}/"
    response = requests.get(url)
    if response.status_code == 200:
        streaming_links = get_streaming_link(response.content)
        if streaming_links:
            reply_text = f"Berikut adalah tautan untuk menonton {anime_title} di Samehadaku:"
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            option_name,
                            url=streaming_link
                        )
                    ]
                    for option_name, streaming_link in streaming_links.items()
                ]
            )
            await m.reply_text(reply_text, reply_markup=reply_markup)
        else:
            await m.reply_text(
                f"Tidak dapat menemukan tautan streaming untuk {anime_title} di Samehadaku."
            )
    else:
        await m.reply_text(
            "Maaf, terjadi kesalahan saat mengambil informasi dari Samehadaku."
        )
