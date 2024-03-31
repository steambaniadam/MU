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
    "attack on titan II": 25777,
    "attack on titan III": 38524,
    "naruto shippuden": 1735,
    "boruto naruto next generations": 34566,
    "fairy tail final series": 38616,
    "sword art online alicization": 36474,
    "demon slayer kimetsu no yaiba mugen train arc": 40748,
    "my hero academia II": 33152,
    "my hero academia III": 36456,
    "my hero academia IV": 38457,
    "one punch man II": 34134,
    "tokyo ghoul re": 36507,
    "dragon ball super": 31964,
    "bleach the diamonddust rebellion": 1659,
}


def find_matching_anime(anime_name):
    for key in ANIME_LIST:
        if anime_name.lower() == key.lower():
            return ANIME_LIST[key]
    return None


@ky.ubot("streaming", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    if len(m.command) > 1:
        anime_name = " ".join(m.command[1:]).strip()
        anime_id = find_matching_anime(anime_name)
        if anime_id is not None:
            try:
                xi = await c.get_inline_bot_results(
                    bot.me.username, f"steam_in {anime_id}"
                )
                await m.delete()
                if xi.results:
                    await c.send_inline_bot_result(
                        m.chat.id,
                        xi.query_id,
                        xi.results[0].id,
                        reply_to_message_id=ReplyCheck(m),
                    )
                else:
                    await m.edit(f"Failed to get streaming link for `{anime_name}`.")
            except Exception as e:
                await m.edit(
                    f"Failed to get streaming link for `{anime_name}`. Error: {e}"
                )
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
            f"Cara menambahkan list : `{m.text} [my anime list id] [nama anime]`"
        )
        return

    anime_name = " ".join(m.command[2:]).strip().lower()
    mal_id = int(m.command[1])

    ANIME_LIST[anime_name] = mal_id
    await m.reply(
        f"Anime `{anime_name}` dengan `{mal_id}` berhasil ditambahkan ke daftar anime."
    )


@ky.ubot("remove_anime", sudo=True)
async def _(c: nlx, m):
    if len(m.command) < 2:
        await m.reply(f"Cara menghapus dari list : `{m.text} [nama_anime]`")
        return

    anime_name = " ".join(m.command[1:]).strip().lower()

    if anime_name not in ANIME_LIST:
        await m.reply(f"Anime `{anime_name}` tidak ada dalam daftar.")
        return

    del ANIME_LIST[anime_name]
    await m.reply(f"Anime `{anime_name}` berhasil dihapus dari daftar anime.")
