################################################################
"""
 Mix-Userbot Open Source . Maintained ? Yes Oh No Oh Yes Ngentot
 
 @ CREDIT : NAN-DEV || William Butcher
 
 EH KONTOL KALO PUNYA AKAL DIPAKE YA ANJING GAUSAH APUS² CREDIT MODAL NYOPAS LO BAJINGAN!!
"""
################################################################


import requests
from pyrogram import *
from pyrogram.types import *

from Mix import *

__modles__ = "IpSearch"
__help__ = get_cgr("help_ips")


def get_ip_info(ip):
    url = "https://ip-geolocation-find-ip-location-and-ip-info.p.rapidapi.com/backend/ipinfo/"
    querystring = {"ip": ip}
    headers = {
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "ip-geolocation-find-ip-location-and-ip-info.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()


def format_ip_info(ip_info):
    em = Emojik()
    em.initialize()
    latitude, longitude = ip_info.get("loc", "0,0").split(",")
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
    formatted_info = ""
    formatted_info += f"• IP Address : `{ip_info.get('ip', 'None')}`\n"
    formatted_info += f"• Hostname : `{ip_info.get('hostname', 'Unknown')}`\n"
    formatted_info += f"• Kota : `{ip_info.get('city', 'Unknown')}`\n"
    formatted_info += f"• Region : `{ip_info.get('region', 'Unknown')}`\n"
    formatted_info += f"• Negara : `{ip_info.get('country_name', 'Unknown')}`\n"
    formatted_info += f"• Lokasi : [Tautan Lokasi]({google_maps_link})\n"
    formatted_info += f"• Kode Pos : `{ip_info.get('postal', 'Unknown')}`\n"
    formatted_info += f"• Zona Waktu : `{ip_info.get('timezone', 'Unknown')}`\n"
    formatted_info += f"• Bendera Negara : `{ip_info.get('country_flag', {}).get('emoji', 'Unknown')}`\n"
    formatted_info += (
        f"• Mata Uang : `{ip_info.get('country_currency', {}).get('code', 'Unknown')}`"
    )

    return formatted_info


@ky.ubot("ipinfo", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        if len(m.command) > 1:
            ip = m.command[1]
            ip_info = get_ip_info(ip)
            formatted_info = format_ip_info(ip_info)
            latitude, longitude = ip_info.get("loc", "0,0").split(",")
            google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Tautan Lokasi", url=google_maps_link)],
                ],
                [[InlineKeyboardButton("Tutup", callback_data="close_ip")]],
            )

            await m.reply(
                f"{em.sukses} Sukses mendapatkan informasi dari IP `{ip}`:\n\n",
                {formatted_info},
                reply_markup=keyboard,
                reply_to_message_id=ReplyCheck(m),
            )
            await pros.delete()
        else:
            await pros.edit(
                cgr("error").format(em.gagal, "Mohon masukkan IP yang valid.")
            )
    except Exception as e:
        await pros.edit(cgr("error").format(em.gagal, str(e)))


@ky.callback("close_ip")
async def _(c, cq):
    await cq.message.delete()


"""
@ky.ubot("ipf|ipfake", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    if len(m.command) == 1 and not rep:
        return await m.reply_text(f"{em.gagal} **Kasih kota nya Kontol!!**")
    if rep:
        ipf = rep.text
    else:
        ipf = m.command[1]
    msg = await m.reply_text(cgr("proses").format(em.proses))
    try:
        meki = SafoneAPI()
        fkip = await meki.fakeinfo(ipf)
        output = f"**Country Info:**\n\n"
        output += f"Name: {fkip['name']['title']} {fkip['name']['first']} {fkip['name']['last']}\n"
        output += f"Gender: {fkip['gender']}\n"
        output += f"Date of Birth: {fkip['dob']['date']}\n"
        output += f"Age: {fkip['dob']['age']}\n"
        output += f"Phone: {fkip['phone']}\n"
        output += f"Cell: {fkip['cell']}\n"
        output += f"Email: {fkip['email']}\n"
        output += (
            f"Location: {fkip['location']['city']}, {fkip['location']['country']}\n"
        )
        output += f"State: {fkip['location']['state']}\n"
        output += f"Postcode: {fkip['location']['postcode']}\n"
        output += f"Timezone: {fkip['location']['timezone']['description']} ({fkip['location']['timezone']['offset']})\n"
    except Exception as er:
        return await msg.edit(cgr("err").format(em.gagal, er))
    await msg.edit(output)
    return


@ky.ubot("ips|ipsearch|ip", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    rep = m.reply_to_message
    if len(m.command) == 1 and not rep:
        return await m.reply_text(f"{em.gagal} **Kasih Ip nya Kontol!!**")
    if rep:
        ip_address = rep.text
    else:
        ip_address = m.command[1]
    msg = await m.reply_text(cgr("proses").format(em.proses))
    try:
        res = await http.get(f"https://ipinfo.io/{ip_address}/json", timeout=5)
    except asyncio.TimeoutError:
        return await msg.edit(f"{em.gagal} Timeout Error!!")
    except Exception as e:
        return await msg.edit(cgr("err").format(em.gagal, e))
    hostname = res.get("hostname", "N/A")
    city = res.get("city", "N/A")
    region = res.get("region", "N/A")
    country = res.get("country", "N/A")
    location = res.get("loc", "N/A")
    org = res.get("org", "N/A")
    await msg.edit(
        (
            f"**Details of `{ip_address}`**\n\n"
            f"HostName: `{hostname}`\n"
            f"City: `{city}`\n"
            f"Region: `{region}`\n"
            f"Country: `{country}`\n"
            f"Org: `{org}`\n"
            f"Map: https://www.google.fr/maps?q={location}\n"
        ),
        disable_web_page_preview=True,
    )
    return
"""
