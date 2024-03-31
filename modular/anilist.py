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
    "bleach": 269,
    "hunter x hunter": 11061,
    "fairy tail": 6702,
    "dragon ball z": 813,
    "cowboy bebop": 1,
}


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


@ky.ubot("anime_list", sudo=True)
async def _(c: nlx, m):
    anime_list_text = "\n".join(
        [f"**{i}) `{name}`" for i, name in enumerate(ANIME_LIST.keys(), start=1)]
    )
    await m.reply(f"**List of available anime:**\n{anime_list_text}")


@ky.ubot("add_anime", sudo=True)
async def _(c: nlx, m):
    if len(m.command) < 3:
        await m.reply(
            f"Cara menambahkan list: `{m.text} [nama anime] [my anime list id]`"
        )
        return

    anime_name = m.command[1].lower()
    mal_id = int(m.command[2])

    ANIME_LIST[anime_name] = mal_id
    await m.reply(
        f"Anime `{anime_name}` dengan `{mal_id}` berhasil ditambahkan ke daftar anime."
    )
