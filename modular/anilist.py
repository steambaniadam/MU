"""
from Mix import *

__modles__ = "AniList"
__help__ = get_cgr("help_animstream")


@ky.ubot("streaming", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) > 1:
        anime_id = m.command[1]
        try:
            xi = await c.get_inline_bot_results(bot.me.username, f"steam_in {anime_id}")
            await m.delete()
            await c.send_inline_bot_result(
                m.chat.id,
                xi.query_id,
                xi.results[0].id,
                reply_to_message_id=ReplyCheck(m),
            )
            await pros.delete()
        except Exception as e:
            await m.edit(f"{e}")
        finally:
            await pros.delete()
"""

import re

from Mix import *

__modles__ = "AniList"
__help__ = get_cgr("help_animstream")


ANIME_LIST = {
    "naruto": 20,
    "attack on titan": 16498,
    "one piece": 21,
    "demon slayer": 38000,
    "my hero academia": 38408,
    "death note": 1535,
    "fullmetal alchemist": 5114,
    "sword art online": 11757,
    "one punch man": 30276,
    "tokyo ghoul": 22319,
}


URL_REGEX = re.compile(
    r"""(?i)\b((?:https?://|www\d{0,3}[.]|
              [a-z0-9.\-][.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|
              (\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\
              ()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""".strip()
)


@ky.ubot("streaming", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) > 1:
        anime_name = " ".join(m.command[1:]).strip().lower()
        if anime_name in ANIME_LIST:
            anime_id = ANIME_LIST[anime_name]
            try:
                xi = await c.get_inline_bot_results(
                    bot.me.username, f"steam_in {anime_id}"
                )
                await m.delete()
                await c.send_inline_bot_result(
                    m.chat.id,
                    xi.query_id,
                    xi.results[0].id,
                    reply_to_message_id=ReplyCheck(m),
                )
                await pros.delete()
            except Exception as e:
                await m.edit(f"{e}")
        else:
            await m.edit("Anime not found in the list.")
    else:
        await m.edit("Please provide the name of the anime.")
    await pros.delete()
