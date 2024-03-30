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
