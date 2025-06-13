import asyncio
import random
import time

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from youtubesearchpython.__future__ import VideosSearch

import config
from AnonXMusic import app
from AnonXMusic.misc import _boot_
from AnonXMusic.plugins.sudo.sudoers import sudoers_list
from AnonXMusic.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from AnonXMusic.utils.decorators.language import LanguageStart
from AnonXMusic.utils.formatters import get_readable_time
from AnonXMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string


hehe_texts = [
    "<b>hey qt</b>",
    "<b>hey qt</b>",
    "<b>hey qt</b>",
]

stickers = [
    "CAACAgQAAxkBAAOGaEv_ZzrEqKiek0wAAXF8FA0AAQFTqgACOgkAAhTL8FDqxvaN6uy7eh4E",
    "CAACAgQAAxkBAAOFaEv_X2id5IFluhjLAAErmzZNH-fsAAJkCgAC2YdhUemgHmR3L623HgQ",
]


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name.startswith("help"):
            keyboard = help_pannel(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name.startswith("sud"):
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} checked <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜID:</b> <code>{message.from_user.id}</code>\n<b>Username:</b> @{message.from_user.username}",
                )
            return
        if name.startswith("inf"):
            m = await message.reply_text("🔎")
            query = name.replace("info_", "", 1)
            results = VideosSearch(f"https://www.youtube.com/watch?v={query}", limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]

            text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=text,
                reply_markup=keyboard,
            )
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} checked <b>ᴛʀᴀᴄᴋ ɪɴғᴏ</b>.\n\n<b>ᴜID:</b> <code>{message.from_user.id}</code>\n<b>Username:</b> @{message.from_user.username}",
                )
            return

    # DEFAULT START
    out = private_panel(_)

    # Step 1: Send hehe message
    m = await message.reply_text(random.choice(hehe_texts))

    await asyncio.sleep(0.75)

    # Step 2: Edit to sticker
    await m.delete()
    s = await message.reply_sticker(random.choice(stickers))

    await asyncio.sleep(1.25)

    # Step 3: Edit to start video message
    await s.delete()
    final = await message.reply_video(
        video="https://files.catbox.moe/bd9lig.mp4",
        caption=_["start_2"].format(message.from_user.mention, app.mention),
        reply_markup=InlineKeyboardMarkup(out),
    )

    # Optional logging
    if await is_on_off(2):
        await app.send_message(
            chat_id=config.LOGGER_ID,
            text=f"{message.from_user.mention} started the bot.\n\n<b>ᴜID:</b> <code>{message.from_user.id}</code>\n<b>Username:</b> @{message.from_user.username}",
        )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_3"].format(
                        message.from_user.first_name,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
