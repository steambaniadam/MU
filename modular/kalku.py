from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Mix import *


@ky.ubot("calc", sudo=True)
async def calc_command(c: nlx, message):
    await message.reply_text(
        "Halo! Saya adalah kalkulator bot. Silakan gunakan tombol-tombol di bawah ini untuk melakukan kalkulasi.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("1", callback_data="1"),
                    InlineKeyboardButton("2", callback_data="2"),
                    InlineKeyboardButton("3", callback_data="3"),
                    InlineKeyboardButton("+", callback_data="+"),
                ],
                [
                    InlineKeyboardButton("4", callback_data="4"),
                    InlineKeyboardButton("5", callback_data="5"),
                    InlineKeyboardButton("6", callback_data="6"),
                    InlineKeyboardButton("-", callback_data="-"),
                ],
                [
                    InlineKeyboardButton("7", callback_data="7"),
                    InlineKeyboardButton("8", callback_data="8"),
                    InlineKeyboardButton("9", callback_data="9"),
                    InlineKeyboardButton("x", callback_data="*"),
                ],
                [
                    InlineKeyboardButton("C", callback_data="C"),
                    InlineKeyboardButton("0", callback_data="0"),
                    InlineKeyboardButton("=", callback_data="="),
                    InlineKeyboardButton("/", callback_data="/"),
                ],
            ]
        ),
    )


@ky.callback("calc_kolbek")
async def button_click(c: nlx, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    try:
        if data == "=":
            expression = callback_query.message.reply_to_message.text.split("=")[0]
            result = eval(expression)
            await c.edit_message_text(
                chat_id=chat_id, message_id=message_id, text=f"{expression} = {result}"
            )
        elif data == "C":
            await c.edit_message_text(chat_id=chat_id, message_id=message_id, text="")
        else:
            await c.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=callback_query.message.reply_to_message.text + data,
            )
    except Exception as e:
        await callback_query.answer(f"Error: {str(e)}")
