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
    formatted_info += f"• City : `{ip_info.get('city', 'Unknown')}`\n"
    formatted_info += f"• Region : `{ip_info.get('region', 'Unknown')}`\n"
    formatted_info += f"• Country : `{ip_info.get('country_name', 'Unknown')}`\n"
    formatted_info += f"• Location : [Location]({google_maps_link})\n"
    formatted_info += f"• Postal Code : `{ip_info.get('postal', 'Unknown')}`\n"
    formatted_info += f"• Timezone : `{ip_info.get('timezone', 'Unknown')}`\n"
    formatted_info += (
        f"• Flag : `{ip_info.get('country_flag', {}).get('emoji', 'Unknown')}`\n"
    )
    formatted_info += (
        f"• Currency : `{ip_info.get('country_currency', {}).get('code', 'Unknown')}`"
    )

    return formatted_info


@ky.ubot("ipinfo", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        pros = await m.reply(cgr("proses").format(em.proses))
        if len(m.command) > 1:
            ip = m.command[1]
            ip_info = get_ip_info(ip)
            formatted_info = format_ip_info(ip_info)
            latitude, longitude = ip_info.get("loc", "0,0").split(",")
            google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Tautan Lokasi", url=google_maps_link)],
                    [InlineKeyboardButton("Tutup", callback_data="close_ip")],
                ]
            )

            await m.reply(
                f"{em.sukses} Sukses mendapatkan informasi dari IP `{ip}`:\n\n{formatted_info}",
                reply_markup=keyboard,
                reply_to_message_id=ReplyCheck(m),
                disable_web_page_preview=True,
            )
            await pros.delete()
        else:
            await pros.edit(
                cgr("err").format(em.gagal, "Mohon masukkan IP yang valid.")
            )
    except Exception as e:
        await pros.edit(cgr("err").format(em.gagal, str(e)))


@ky.callback("close_ip")
async def _(c, cq):
    await cq.message.delete()


def generate_temp_gmail():
    url = "https://temporary-gmail-account.p.rapidapi.com/GmailGetAccount"
    payload = {"generateNewAccount": 1}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temporary-gmail-account.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


async def format_temp_gmail(temp_gmail_info):
    if "address" in temp_gmail_info and "token" in temp_gmail_info:
        return f"Success Generated Temp Gmail :\nEmail : `{temp_gmail_info['address']}`\nToken : `{temp_gmail_info['token']}`"
    else:
        raise ValueError("Missing address or token in temporary Gmail account info")


@ky.ubot("genmail", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        temp_gmail_info = generate_temp_gmail()
        formatted_temp_gmail_info = await format_temp_gmail(temp_gmail_info)
        await pros.edit(f"{em.sukses} {formatted_temp_gmail_info}")
    except Exception as e:
        await pros.edit(f"{em.gagal} {str(e)}")


def get_messages_temp_email(gmail, token):
    url = "https://temporary-gmail-account.p.rapidapi.com/GmailGetMessages"
    payload = {
        "address": gmail,
        "token": token,
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temporary-gmail-account.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


async def format_messages(messages):
    if "totalItems" in messages and "member" in messages:
        total_items = messages["totalItems"]
        member = messages["member"]
        formatted_messages = f"Inbox {member[0]['to']['address']}:\n\n"
        formatted_messages += f"Total Pesan Masuk : {total_items}\n"
        formatted_messages += f"Tipe Pesan : {member[0]['@type']}\n"
        formatted_messages += f"ID Pesan : {member[0]['msgid']}\n"
        formatted_messages += f"Pesan Dari : {member[0]['from']['name']}\n"
        formatted_messages += f"Email Pengirim : {member[0]['from']['address']}\n\n"
        formatted_messages += f"Refreshed on : {member[0]['updatedAt']}"
        return formatted_messages
    else:
        raise ValueError("Missing 'totalItems' or 'member' key in messages")


@ky.ubot("getmail", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        if len(m.command) >= 3:
            gmail = m.command[1]
            token = m.command[2]
            messages = get_messages_temp_email(gmail, token)
            formatted_messages = await format_messages(messages)
            await pros.edit(f"{em.sukses} {formatted_messages}")
        else:
            await pros.edit(f"{em.gagal} Mohon masukkan Gmail dan token yang valid.")
    except Exception as e:
        await pros.edit(f"{em.gagal} {str(e)}")


# COMING SOON! LIMIT BRE!
def get_message(messid, addres, token):
    url = "https://temporary-gmail-account.p.rapidapi.com/GmailGetMessage"

    payload = {
        "messageId": "messageId provided by GetMessages",
        "address": "Gmail address generated by GetAccount",
        "token": "Token generated by GetAccount",
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temporary-gmail-account.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def gen_temp_mail():
    url = "https://temp-mail44.p.rapidapi.com/api/v3/email/new"
    payload = {"key1": "value", "key2": "value"}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


async def format_temp_mail(temp_mail):
    if "email" in temp_mail and "token" in temp_mail:
        return f"Success Generated Temp Mail :\nEmail : `{temp_mail['email']}`\nToken : `{temp_mail['token']}`"
    else:
        raise ValueError("Missing address or token in temporary Gmail account info")


@ky.ubot("tempmail", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    pros = await m.reply(cgr("proses").format(em.proses))
    try:
        temp_gmail_info = gen_temp_mail()
        formatted_temp_mail = await format_temp_mail(temp_gmail_info)
        await pros.edit(f"{em.sukses} {formatted_temp_mail}")
    except Exception as e:
        await pros.edit(f"{em.gagal} {str(e)}")


def get_temp_messages(email):
    url = f"https://temp-mail44.p.rapidapi.com/api/v3/email/{email}/messages"
    headers = {
        "X-RapidAPI-Key": "24d6a3913bmsh3561d6af783658fp1a8240jsneef57a49ff14",
        "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    return response.json()


async def format_temp_messages(messages):
    formatted_messages = ""
    for email in messages:
        formatted_messages += f"ID Pesan : {email['id']}\n"
        formatted_messages += f"Pesan Dari : {email['from']}\n"
        formatted_messages += f"Tujuan : {email['to']}\n"
        formatted_messages += f"CC : {email.get('cc', 'Unknown')}\n"
        formatted_messages += f"Subjek : {email['subject']}\n"
        formatted_messages += f"Isi Teks : {email['body_text']}\n"
        formatted_messages += f"Tanggal Dibuat : {email['created_at']}\n\n"
    return formatted_messages


@ky.ubot("gettemp", sudo=True)
async def _(c: nlx, m):
    em = Emojik()
    em.initialize()
    try:
        if len(m.command) > 1:
            email = m.command[1]
            messages = get_temp_messages(email)
            formatted_messages = await format_temp_messages(messages)
            await m.reply(formatted_messages)
        else:
            await m.reply("Mohon berikan alamat email sebagai argumen.")
    except Exception as e:
        await m.reply(f"{em.gagal} Gagal mengambil pesan sementara: {str(e)}")



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
