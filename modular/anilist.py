import requests
from pyrogram import *

from Mix import *

__modles__ = "Anime List"
__help__ = "Anime List"


@ky.ubot("anilist", sudo=True)
async def anilist_command(c: nlx, m):
    m.chat.id
    message_id = m.message_id

    args = m.command
    if len(args) < 2:
        await m.reply_text("Please provide the name of the anime.")
        return

    anime_title = " ".join(args[1:])

    url = f"https://api.jikan.moe/v4/anime?q={anime_title}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            anime_info = data[0]
            title = anime_info["title"]
            synopsis = anime_info["synopsis"]
            episodes = anime_info["episodes"]
            score = anime_info["score"]
            url = anime_info["url"]
            message_text = f"Title: {title}\nSynopsis: {synopsis}\nEpisodes: {episodes}\nScore: {score}\nURL: {url}"
            await m.reply_text(message_text, reply_to_message_id=message_id)
        else:
            await m.reply_text("Anime not found.")
    else:
        await m.reply_text(
            f"Failed to fetch data. Status code: {response.status_code}",
            reply_to_message_id=message_id,
        )
