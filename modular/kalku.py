from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Mix import *


@ky.ubot(["calc", "kalkulator"], sudo=True)
async def _(c: nlx, message):
    await message.reply_text(
        " ",
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


@ky.callbck()
async def _(c: nlx, cq):
    data = cq.data
    chat_id = cq.message.chat.id
    message_id = cq.message.id

    try:
        if data == "=":
            expression = cq.message.reply_to_message.text.split("=")[0]
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
                text=cq.message.reply_to_message.text + data,
            )
    except Exception as e:
        await cq.answer(f"Error: {str(e)}")
