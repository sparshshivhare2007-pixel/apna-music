from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

from config import API_ID, API_HASH, SESSION_STRING
from helpers.downloader import download_audio
from helpers.queue import add_to_queue, pop_from_queue

app = Client(session_name=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(app)

# Mapping: chat_id -> current playing track
current_track = {}

@app.on_message(filters.command("start"))
async def start_cmd(client, message: Message):
    await message.reply_text("👋 Hello! Send /play <youtube-url> to play music in VC.")

@app.on_message(filters.command("play"))
async def play_cmd(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /play <youtube-url>")
        return

    url = message.command[1]
    chat_id = message.chat.id
    msg = await message.reply_text("Downloading audio...")

    try:
        path = download_audio(url)
        add_to_queue(chat_id, path)
        await msg.edit_text(f"Added to queue: {path.stem}")

        # If nothing is playing, start VC streaming
        if chat_id not in current_track:
            track = pop_from_queue(chat_id)
            if track:
                current_track[chat_id] = track
                await pytgcalls.join_group_call(
                    chat_id,
                    AudioPiped(str(track))
                )
    except Exception as e:
        await msg.edit_text(f"Error: {e}")

# Voice call finished handler
@pytgcalls.on_stream_end()
async def on_stream_end(_, update):
    chat_id = update.chat_id
    next_track = pop_from_queue(chat_id)
    if next_track:
        current_track[chat_id] = next_track
        await pytgcalls.change_stream(chat_id, AudioPiped(str(next_track)))
    else:
        current_track.pop(chat_id, None)
        await pytgcalls.leave_group_call(chat_id)

app.start()
pytgcalls.start()
print("Bot is running...")
app.idle()
