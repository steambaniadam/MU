from Mix import *

__modles__ = "Anime Streaming"
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
