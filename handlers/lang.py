from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from solidAPI import set_lang
from solidAPI.other import kode, lang_flags, get_message

from utils.decorators import authorized_only
from utils.functions import group_only


@Client.on_message(filters.command("lang") & group_only)
@authorized_only
async def change_lang(_, message: Message):
    try:
        lang = message.command[1]
    except IndexError:
        lang = ""
    if len(lang) > 2 or len(lang) == 1:
        await message.reply(get_message(message.chat.id, "error_lang_cmd"))
        return
    if not lang:
        temp = []
        keyboard = []
        for count, j in enumerate(kode, start=1):
            temp.append(
                InlineKeyboardButton(f"{lang_flags[j]}", callback_data=f"set_lang_{j}")
            )
            if count % 2 == 0:
                keyboard.append(temp)
                temp = []
            if count == len(kode):
                keyboard.append(temp)
        await message.reply(
            get_message(message.chat.id, "supported_lang"),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    if len(lang) == 2:
        if lang in kode:
            x = set_lang(message.chat.id, lang)
            if x == 200:
                await message.reply(get_message(message.chat.id, "lang_changed"))
            elif x == 404:
                await message.reply(get_message(message.chat.id, "error_change_lang"))
        else:
            await message.reply(get_message(message.chat.id, "not_supported_lang"))
