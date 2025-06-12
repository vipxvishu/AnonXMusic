from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database import add_sudo, remove_sudo
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.extraction import extract_user
from AnonXMusic.utils.inline import close_markup
from config import BANNED_USERS, OWNER_ID

# 🔒 Protected User ID
PROTECTED_USER = 6748827895


# ─── Add Sudo ─────────────────────────────
@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
@language
async def useradd(_, message: Message, _str):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_str["general_1"])

    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(_str["sudo_1"].format(user.mention))

    if await add_sudo(user.id):
        SUDOERS.add(user.id)
        return await message.reply_text(_str["sudo_2"].format(user.mention))
    return await message.reply_text(_str["sudo_8"])


# ─── Remove Sudo ──────────────────────────
@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID))
@language
async def userdel(_, message: Message, _str):
    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text(_str["general_1"])

    user = await extract_user(message)

    if user.id == PROTECTED_USER:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("okay", callback_data="ok_protect"),
                    InlineKeyboardButton("sad", callback_data="sad_protect"),
                ]
            ]
        )
        return await message.reply_text(
            text="🚫 <b>ᴋɴᴏᴡ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴅᴏɪɴɢ ʙᴇғᴏʀᴇ ʏᴏᴜ ᴘʀᴏᴄᴇᴇᴅ.</b>\n\nThis user is 𝙛𝙪𝙡𝙡ʏ 𝙥𝙧𝙤𝙩𝙚𝙘𝙩𝙚𝙙.",
            reply_markup=buttons
        )

    if user.id not in SUDOERS:
        return await message.reply_text(_str["sudo_3"].format(user.mention))

    if await remove_sudo(user.id):
        SUDOERS.remove(user.id)
        return await message.reply_text(_str["sudo_4"].format(user.mention))
    return await message.reply_text(_str["sudo_8"])


# ─── Sudo List ─────────────────────────────
@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"]) & ~BANNED_USERS)
@language
async def sudoers_list(_, message: Message, _str):
    text = _str["sudo_5"]
    user = await app.get_users(OWNER_ID)
    owner = user.mention if user.mention else user.first_name
    text += f"1➤ {owner}\n"

    count = 0
    line_open = False
    for user_id in SUDOERS:
        if user_id != OWNER_ID:
            try:
                user = await app.get_users(user_id)
                mention = user.mention if user.mention else user.first_name
                if not line_open:
                    text += _str["sudo_6"]
                    line_open = True
                count += 1
                text += f"{count}➤ {mention}\n"
            except:
                continue

    return await message.reply_text(
        text if count > 0 else _str["sudo_7"],
        reply_markup=close_markup(_str)
    )


# ─── Callbacks ─────────────────────────────
@app.on_callback_query(filters.regex("ok_protect"))
async def protect_ok(_, query: CallbackQuery):
    await query.message.edit_text("<b>okay ! good ,🎀</b>")
    await query.answer()


@app.on_callback_query(filters.regex("sad_protect"))
async def protect_sad(_, query: CallbackQuery):
    await query.message.edit_text("😿 <i>Bye Bye Sir 😭</i>")
    await query.answer("Bot entering infinite loop...")

    # 🌀 Lock loop - simulate soft crash
    while True:
        pass
