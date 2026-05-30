import asyncio
import random

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped


# ---------------- CONFIG ----------------
TOKEN = "8994631118:AAEeRgCZUicKU0_xqVbga2m7rMBoc-KIGFw"

CHANNELS = ["@GAlactic_fire_offi", "@TSS_ints"]
CHANNEL_LINKS = [
    "https://t.me/GAlactic_fire_offi",
    "https://t.me/TSS_ints"
]

ADMIN_ID = 7787618546


# ---------------- SONG DATABASE ----------------
SONGS = {
    "sad": ["Sad Song 1", "Sad Song 2", "Sad Song 3"],
    "lofi": ["Lofi Chill 1", "Lofi Chill 2", "Lofi Chill 3"],
    "party": ["Party Song 1", "Party Song 2", "Party Song 3"],
    "gaming": ["Gaming Beat 1", "Gaming Beat 2", "Gaming Beat 3"],
    "romantic": ["Romantic Song 1", "Romantic Song 2"]
}


# ---------------- VC SYSTEM ----------------
ASSISTANT = Client("tss_music")
call = PyTgCalls(ASSISTANT)

SESSIONS = {}


# ---------------- START VC ----------------
async def start_vc():
    await ASSISTANT.start()
    await call.start()
    print("🎧 VC SYSTEM STARTED")


# ---------------- FORCE JOIN CHECK ----------------
async def is_joined(bot, user_id):
    try:
        for ch in CHANNELS:
            m = await bot.get_chat_member(ch, user_id)
            if m.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False


# ---------------- PLAY SONG ----------------
async def play_song(chat_id, song):
    try:
        await call.join_group_call(
            chat_id,
            AudioPiped(song)
        )
    except Exception as e:
        print("VC ERROR:", e)


# ---------------- AUTO NEXT SONG ----------------
async def next_song(chat_id, context):
    if chat_id not in SESSIONS:
        return

    data = SESSIONS[chat_id]
    playlist = data["playlist"]

    if data["index"] >= len(playlist):
        playlist = random.sample(playlist, len(playlist))
        data["playlist"] = playlist
        data["index"] = 0

    song = playlist[data["index"]]
    data["index"] += 1

    await play_song(chat_id, song)

    await context.bot.send_message(
        chat_id,
        f"🎵 Now Playing: {song}\n\n⚡ Powered By TSS"
    )

    await asyncio.sleep(5)
    await next_song(chat_id, context)


# ---------------- START CATEGORY PLAY ----------------
async def start_play(chat_id, category, context, user):
    playlist = SONGS.get(category, [])

    if not playlist:
        return

    SESSIONS[chat_id] = {
        "playlist": random.sample(playlist, len(playlist)),
        "index": 0,
        "category": category,
        "user": user.id
    }

    await context.bot.send_message(
        chat_id,
        f"🎧 Auto Play Started: {category}\n\n⚡ Powered By TSS"
    )

    await next_song(chat_id, context)


# ---------------- /c COMMAND ----------------
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # FORCE JOIN
    if not await is_joined(context.bot, user.id):
        buttons = [
            [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_LINKS[0])],
            [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_LINKS[1])]
        ]

        await update.message.reply_text(
            "❌ Join both channels first to use bot",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    msg = update.message.text.split()

    if len(msg) < 3:
        return await update.message.reply_text("Use: /c <category> -ap")

    category = msg[1].lower()

    chat_id = update.effective_chat.id

    await start_play(chat_id, category, context, user)


# ---------------- CATEGORY LIST ----------------
async def categories(update, context):
    await update.message.reply_text(
        "🎵 Categories:\n" +
        "\n".join(SONGS.keys()) +
        "\n\n⚡ Powered By TSS"
    )


# ---------------- STOP ----------------
async def stop(update, context):
    chat_id = update.effective_chat.id

    if chat_id in SESSIONS:
        del SESSIONS[chat_id]

    await update.message.reply_text(
        "⛔ Music Stopped\n\n⚡ Powered By TSS"
    )


# ---------------- BROADCAST ----------------
async def broadcast(update, context):
    if update.effective_user.id != ADMIN_ID:
        return

    msg = " ".join(context.args)

    await update.message.reply_text(
        f"📢 {msg}\n\n⚡ Powered By TSS"
    )


# ---------------- BOT SETUP ----------------
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("c", play))
app.add_handler(CommandHandler("categories", categories))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("b", broadcast))


# ---------------- RUN BOT ----------------
async def main():
    await start_vc()
    print("🎧 TSS MUSIC BOT RUNNING...")
    await app.run_polling()


asyncio.run(main())
