import asyncio
import os

from pyrogram.enums import MessagesFilter
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import InputMediaPhoto

from Mix import *

__modles__ = "Convert"
__help__ = get_cgr("help_konpert")


@ky.ubot("toanime", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    pros = await message.reply(cgr("proses").format(em.proses))
    if message.reply_to_message:
        if len(message.command) < 2:
            if message.reply_to_message.photo:
                get_photo = message.reply_to_message.photo.file_id
            elif message.reply_to_message.sticker:
                get_photo = await c.dln(message.reply_to_message)
            elif message.reply_to_message.animation:
                get_photo = await c.dln(message.reply_to_message)
            else:
                return await pros.edit(cgr("konpert_1").format(em.gagal))
        else:
            if message.command[1] in ["foto", "profil", "photo"]:
                chat = (
                    message.reply_to_message.from_user
                    or message.reply_to_message.sender_chat
                )
                get = await c.get_chat(chat.id)
                photo = get.photo.big_file_id
                get_photo = await c.dln(photo)
    else:
        if len(message.command) < 2:
            return await pros.edit(cgr("konpert_1").format(em.gagal))
        else:
            try:
                get = await c.get_chat(message.command[1])
                photo = get.photo.big_file_id
                get_photo = await c.dln(photo)
            except Exception as error:
                return await pros.edit(cgr("err").format(em.gagal, error))
    await pros.edit(cgr("konpert_2").format(em.proses))
    await c.unblock_user("@qq_neural_anime_bot")
    send_photo = await c.send_photo("@qq_neural_anime_bot", get_photo)
    await asyncio.sleep(30)
    await send_photo.delete()
    await pros.delete()
    info = await c.resolve_peer("@qq_neural_anime_bot")
    anime_photo = []
    async for anime in c.search_messages(
        "@qq_neural_anime_bot", filter=MessagesFilter.PHOTO
    ):
        anime_photo.append(
            InputMediaPhoto(
                anime.photo.file_id,
                caption=cgr("konpert_3").format(em.sukses, c.me.mention),
            )
        )
    if anime_photo:
        await c.send_media_group(
            message.chat.id,
            anime_photo,
            reply_to_message_id=message.id,
        )
        return await c.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))

    else:
        await c.send_message(
            message.chat.id,
            cgr("konpert_4").format(em.gagal),
            reply_to_message_id=message.id,
        )
        return await c.invoke(DeleteHistory(peer=info, max_id=0, revoke=True))


@ky.ubot("toimg", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    try:
        pros = await message.reply(cgr("proses").format(em.proses))
        file_io = await c.dln(message.reply_to_message)
        file_io.name = "sticker.png"
        await c.send_photo(
            message.chat.id,
            file_io,
            caption=cgr("konpert_5").format(em.sukses, c.me.mention),
            reply_to_message_id=message.id,
        )
        await pros.delete()
    except Exception as e:
        await pros.delete()
        return await c.send_message(
            message.chat.id,
            cgr("err").format(em.gagal, e),
            reply_to_message_id=message.id,
        )


@ky.ubot("tosticker|tostick", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            return await message.reply_text(cgr("konpert_1").format(em.gagal))
        sticker = await c.download_media(
            message.reply_to_message.photo.file_id,
            f"sticker_{message.from_user.id}.webp",
        )
        await message.reply_sticker(sticker)
        os.remove(sticker)
    except Exception as e:
        await message.reply_text(cgr("err").format(em.gagal, e))


@ky.ubot("togif", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    pros = await message.reply(cgr("proses").format(em.proses))
    if not message.reply_to_message.sticker:
        return await pros.edit(cgr("konpert_6").format(em.gagal))
    await pros.edit(cgr("konpert_2").format(em.proses))
    file = await c.download_media(
        message.reply_to_message,
        f"gift_{message.from_user.id}.mp4",
    )
    try:
        await c.send_animation(message.chat.id, file, reply_to_message_id=message.id)
        os.remove(file)
        await pros.delete()
        return
    except Exception as error:
        await pros.edit(cgr("err").format(em.gagal, star(error)))
        return


@ky.ubot("toaudio", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    replied = message.reply_to_message
    pros = await message.reply(cgr("proses").format(em.proses))
    if not replied:
        return await pros.edit(cgr("konpert_7").format(em.gagal))
    if replied.video:
        await pros.edit(cgr("konpert_2").format(em.proses))
        file = await c.download_media(
            message=replied,
            file_name=f"toaudio_{replied.id}",
        )
        out_file = f"{file}.mp3"
        try:
            await pros.edit(cgr("konpert_8").format(em.proses))
            cmd = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await c.run_cmd(cmd)
            await pros.edit(cgr("konpert_9").format(em.proses))
            await c.send_voice(
                message.chat.id,
                voice=out_file,
                caption=cgr("konpert_5").format(em.sukses, c.me.mention),
                reply_to_message_id=message.id,
            )
            os.remove(file)
            os.remove(out_file)
            return await pros.delete()
        except Exception as error:
            os.remove(file)
            os.remove(out_file)
            return await pros.edit(str(error))
    else:
        os.remove(file)
        os.remove(out_file)
        return await pros.edit(cgr("konpert_7").format(em.gagal))


"""
get_efek = {
    "bengek": '-filter_complex "rubberband=pitch=1.5"',
    "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
    "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
    "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
    "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
    "tremolo": '-filter_complex "tremolo=f=5:d=0.5"',
    "reverse": '-filter_complex "areverse"',
    "flanger": '-filter_complex "flanger"',
    "pitch_up": '-filter_complex "rubberband=pitch=2.0"',
    "pitch_down": '-filter_complex "rubberband=pitch=0.5"',
    "high_pass": '-filter_complex "highpass=f=200"',
    "low_pass": '-filter_complex "lowpass=f=1000"',
    "band_pass": '-filter_complex "bandpass=f=500:width_type=h:w=100"',
    "band_reject": '-filter_complex "bandreject=f=1000:width_type=h:w=100"',
    "fade_in": '-filter_complex "afade=t=in:ss=0:d=5"',
    "fade_out": '-filter_complex "afade=t=out:st=5:d=5"',
    "chorus": '-filter_complex "chorus=0.7:0.9:55:0.4:0.25:2"',
    "vibrato": '-filter_complex "vibrato=f=10"',
    "phaser": '-filter_complex "aphaser=type=t:gain=0.2"',
    "reverb": '-filter_complex "[0] [1] afir=dry=10:wet=10 [reverb]; [0] [reverb] amix=inputs=2:weights=10 1"',
    "distortion": '-filter_complex "distortion=gain=6"',
    "bitcrush": '-filter_complex "acrusher=level_in=10:level_out=16:bits=4:mode=log:aa=1"',
    "wahwah": '-filter_complex "wahwah"',
    "compressor": '-filter_complex "compand=0.3|0.8:6:-70/-70/-20/-20/-20/-20:6:0:-90:0.2"',
    "delay": '-filter_complex "adelay=1000|1000"',
    "stereo_widen": '-filter_complex "stereowiden=level_in=0.5:level_out=1.0:delay=20:width=40"',
    "phaser2": '-filter_complex "aphaser=type=t:decay=1"',
    "reverse_echo": '-filter_complex "aecho=0.8:0.88:1000:0.5"',
    "low_pitch": '-filter_complex "rubberband=pitch=0.7"',
    "high_pitch": '-filter_complex "rubberband=pitch=1.3"',
    "megaphone": '-filter_complex "amix=inputs=2:duration=first:dropout_transition=2,volume=volume=3"',
    "telephone": '-filter_complex "amix=inputs=2:duration=first:dropout_transition=2,volume=volume=1.5"',
    "radio": '-filter_complex "amix=inputs=2:duration=first:dropout_transition=2,volume=volume=2.5"',
}
"""


get_efek = {
    "band_pass": '-filter_complex "bandpass=f=500:width_type=h:w=100"',
    "band_reject": '-filter_complex "bandreject=f=1000:width_type=h:w=100"',
    "bengek": '-filter_complex "rubberband=pitch=1.5"',
    "bitcrush": '-filter_complex "acrusher=level_in=10:level_out=16:bits=4:mode=log:aa=1"',
    "chorus": '-filter_complex "chorus=0.7:0.9:55:0.4:0.25:2"',
    "compressor": '-filter_complex "compand=points=-90/-90|-70/-70|-40/-20|0/-20:delay=0:attack=0.3:release=0.1"',
    "delay": '-filter_complex "adelay=500|500"',
    "distortion": '-filter_complex "apulsator=mode=sine:attack=0.1:decay=1:frequency=4:depth=0.8"',
    "echo": '-filter_complex "aecho=0.8:0.9:500|1000:0.2|0.1"',
    "fade_in": '-filter_complex "afade=t=in:st=0:d=5"',
    "fade_out": '-filter_complex "afade=t=out:st=150:d=5"',
    "fast": "-filter_complex \"afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*3.14)':imag='hypot(re,im)*sin((random(1)*2-1)*2*3.14)':win_size=128:overlap=0.8\"",
    "flanger": '-filter_complex "afftfilt=real=\'hypot(re,im)*cos(PI*2*t*0.05)*0.7\':imag=\'hypot(re,im)*sin(PI*2*t*0.05)*0.7\':win_size=512:overlap=0.75"',
    "high_pass": '-filter_complex "highpass=f=200"',
    "high_pitch": '-filter_complex "rubberband=pitch=1.1"',
    "jedug": '-filter_complex "acrusher=level_in=8:level_out=18:bits=8:mode=log:aa=1"',
    "low_pass": '-filter_complex "lowpass=f=1000"',
    "low_pitch": '-filter_complex "rubberband=pitch=0.7"',
    "megaphone": '-filter_complex "afftfilt=real=\'hypot(re,im)*cos((random(0)*2-1)*2*3.14)\':imag=\'hypot(re,im)*sin((random(1)*2-1)*2*3.14)\':win_size=512:overlap=0.75"',
    "phaser": '-filter_complex "aphaser=type=t"',
    "phaser2": '-filter_complex "aphaser=type=t:decay=0.5"',
    "pitch_down": '-filter_complex "rubberband=pitch=0.5"',
    "pitch_up": '-filter_complex "rubberband=pitch=2.0"',
    "radio": '-filter_complex "amix=inputs=2:duration=first:dropout_transition=2,volume=volume=2.5"',
    "reverb": '-filter_complex "afir=dry=10:wet=10"',
    "reverse": '-filter_complex "areverse"',
    "reverse_echo": '-filter_complex "aecho=0.8:0.88:1000:0.5"',
    "robot": "-filter_complex \"afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75\"",
    "stereo_widen": '-filter_complex "stereowiden=level_in=0.5:level_out=1.0:delay=20:width=40"',
    "telephone": '-filter_complex "amix=inputs=2:duration=first:dropout_transition=2,volume=volume=1.5"',
    "tremolo": '-filter_complex "tremolo=f=5:d=0.5"',
    "vibrato": '-filter_complex "vibrato=f=10"',
    "wahwah": '-filter_complex "wahwah"',
}


list_efek = [
    "band_pass",
    "band_reject",
    "bengek",
    "bitcrush",
    "chorus",
    "compressor",
    "delay",
    "distortion",
    "echo",
    "fade_in",
    "fade_out",
    "fast",
    "flanger",
    "high_pass",
    "high_pitch",
    "jedug",
    "low_pass",
    "low_pitch",
    "megaphone",
    "phaser",
    "phaser2",
    "pitch_down",
    "pitch_up",
    "radio",
    "reverb",
    "reverse",
    "reverse_echo",
    "robot",
    "stereo_widen",
    "telephone",
    "tremolo",
    "vibrato",
    "wahwah",
]


list_efek_deskripsi = {
    "band_pass": "Hanya melewati frekuensi tertentu.",
    "band_reject": "Memblokir frekuensi tertentu.",
    "bengek": "Suara seperti berbicara dengan mulut penuh.",
    "bitcrush": "Resolusi sampel berkurang.",
    "chorus": "Efek suara banyak.",
    "compressor": "Mengurangi dinamika suara.",
    "delay": "Mengulang suara dengan jeda waktu.",
    "distortion": "Suara terdistorsi.",
    "echo": "Efek gema atau pantulan suara.",
    "fade_in": "Meningkatkan volume bertahap.",
    "fade_out": "Mengurangi volume bertahap.",
    "fast": "Mempercepat suara.",
    "flanger": "Efek modulasi pada suara.",
    "high_pass": "Menghilangkan frekuensi rendah.",
    "high_pitch": "Meningkatkan pitch suara.",
    "jedug": "Efek kedapatan suara.",
    "low_pass": "Menghilangkan frekuensi tinggi.",
    "low_pitch": "Menurunkan pitch suara.",
    "megaphone": "Suara seperti megaphone.",
    "phaser": "Efek suara bergetar.",
    "phaser2": "Variasi efek phaser.",
    "pitch_down": "Menurunkan nada suara.",
    "pitch_up": "Meningkatkan nada suara.",
    "radio": "Suara seperti radio.",
    "reverb": "Efek suara gema.",
    "reverse": "Memutar suara ke belakang.",
    "reverse_echo": "Pantulan suara terbalik.",
    "robot": "Suara seperti robot.",
    "stereo_widen": "Suara terdengar lebih luas.",
    "telephone": "Suara seperti telepon.",
    "tremolo": "Efek getaran pada suara.",
    "vibrato": "Efek getaran kecil.",
    "wahwah": "Efek suara wah-wah.",
}


@ky.ubot("list-efek|efeks|list-effects", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()

    daftar_efek = "\n".join(
        [
            f"• `{epek}` - `{list_efek_deskripsi.get(epek, 'Coba Sendiri')}`"
            for epek in list_efek
        ]
    )

    await message.reply(cgr("konpert_10").format(em.sukses, daftar_efek))


@ky.ubot("efek|effect|voifek", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    args = c.get_arg(message)
    reply = message.reply_to_message
    prefix = await c.get_prefix(c.me.id)
    pros = await message.reply(cgr("konpert_11").format(em.proses, args))
    if reply and args in get_efek:
        indir = await c.download_media(reply, file_name="audio.mp3")
        converted_file = "converted_audio.mp3"
        ses = await asyncio.create_subprocess_shell(
            f"ffmpeg -i '{indir}' {get_efek[args]} {converted_file}"
        )
        await ses.communicate()
        await message.reply_voice(
            open(f"{converted_file}", "rb"),
            caption=cgr("konpert_12").format(em.sukses, args),
        )
        for files in (f"{converted_file}", indir):
            if files and os.path.exists(files):
                os.remove(files)
                os.remove(indir)
        await pros.delete()
    else:
        await pros.edit(cgr("konpert_13").format(em.gagal, next((p) for p in prefix)))


"""
@ky.ubot("efek|effect|voifek", sudo=True)
async def _(c: nlx, message):
    em = Emojik()
    em.initialize()
    args = c.get_arg(message)
    reply = message.reply_to_message
    prefix = await c.get_prefix(c.me.id)
    pros = await message.reply(cgr("konpert_11").format(em.proses, args))
    if reply and list_efek:
        if args in list_efek:
            indir = await c.download_media(reply, file_name=f"{c.me.id}.mp3")
            ses = await asyncio.create_subprocess_shell(
                f"ffmpeg -i '{indir}' {get_efek[args]} audio.mp3"
            )
            await ses.communicate()
            await message.reply_voice(
                open("audio.mp3", "rb"),
                caption=cgr("konpert_12").format(em.sukses, args)),
            for files in ("audio.mp3", indir):
                if files and os.path.exists(files):
                    os.remove(files)
            await pros.delete()
        else:
            await pros.edit(
                cgr("konpert_13").format(em.gagal, next((p) for p in prefix))
            )
    else:
        await pros.edit(cgr("konpert_13").format(em.gagal, next((p) for p in prefix)))
"""
