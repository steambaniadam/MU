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


def get_video_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        iframe = soup.find("iframe")
        if iframe and "src" in iframe.attrs:
            video_src = iframe["src"]
            return video_src
        else:
            return None
    else:
        return None


def get_streaming_links(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    streaming_links = {}
    divs = soup.find_all("div", class_="streaming-option")
    for div in divs:
        option_name = div.find("span").text.strip()
        link = div["data-src"]
        streaming_links[option_name] = link
    return streaming_links


@ky.ubot("anilist")
async def anilist_command(c: nlx, m):
    if len(m.command) < 3:
        await m.reply_text(
            f"Silakan masukkan judul anime dan episode setelah perintah `{m.text}` [judul anime] [episode]"
        )
        return

    anime_title = "-".join(m.command[1:-1])
    episode = m.command[-1]
    url = f"https://oploverz.news/{anime_title}-episode-{episode}/"
    response = requests.get(url)
    if response.status_code == 200:
        streaming_links = get_streaming_links(response.content)
        if streaming_links:
            for option_name, link in streaming_links.items():
                video_url = get_video_url(link)
                if video_url:
                    anime_title_display = " ".join(m.command[1:-1])
                    reply_text = f"Berikut adalah tautan untuk menonton `{anime_title_display}` episode `{episode}` di Oploverz ({option_name}):"
                    reply_markup = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text=f"Streaming di Oploverz ({option_name})",
                                    url=video_url,
                                )
                            ]
                        ]
                    )
                    await m.reply_text(reply_text, reply_markup=reply_markup)
                    break  # Hanya ambil tautan dari opsi pertama yang berhasil
            else:
                await m.reply_text(
                    f"Tidak dapat menemukan tautan video untuk {anime_title} episode {episode} di Oploverz."
                )
        else:
            await m.reply_text(
                f"Tidak dapat menemukan opsi pemutar untuk {anime_title} episode {episode} di Oploverz."
            )
    else:
        await m.reply_text(
            "Maaf, terjadi kesalahan saat mengambil informasi dari Oploverz."
        )
