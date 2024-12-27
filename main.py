import discord
from discord.ext import commands
from embed_handler import MusicButtons, update_embed
from discord import FFmpegPCMAudio
import yt_dlp as youtube_dl
import asyncio
import sqlite3

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Database setup
conn = sqlite3.connect("music_bot.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS server_data (
    server_id INTEGER PRIMARY KEY,
    channel_id INTEGER
)
""")
conn.commit()

# FFmpeg options
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Song queue and voice client
song_queues = {}
voice_clients = {}
current_volumes = {}

# Function to get audio URL
async def get_audio_url(query):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info['entries'][0]['url'], info['entries'][0]['title']

# Play command
@bot.command(aliases=["p"])
async def play(ctx, *, query: str):
    server_id = ctx.guild.id
    if server_id not in song_queues:
        song_queues[server_id] = []

    if not ctx.author.voice:
        await ctx.send("You need to join a voice channel first!")
        return

    song_url, song_name = await get_audio_url(query)

    if server_id not in voice_clients or not voice_clients[server_id].is_connected():
        for _ in range(3):
            try:
                voice_clients[server_id] = await ctx.author.voice.channel.connect(timeout=10, reconnect=True)
                break
            except asyncio.TimeoutError:
                await ctx.send("Failed to connect to the voice channel. Retrying...")
        else:
            await ctx.send("Could not connect to the voice channel after multiple attempts.")
            return

    if voice_clients[server_id].is_playing() or voice_clients[server_id].is_paused():
        song_queues[server_id].append((song_url, song_name))
        await ctx.send(f"Added to queue: {song_name}")
        return

    source = FFmpegPCMAudio(song_url, **ffmpeg_options)
    volume = current_volumes.get(server_id, 1.0)
    source = discord.PCMVolumeTransformer(source, volume)

    try:
        voice_clients[server_id].play(source, after=lambda e: asyncio.run_coroutine_threadsafe(next_song(ctx), bot.loop))
    except Exception as e:
        await ctx.send(f"Error starting playback: {e}")
        return

    await bot.change_presence(activity=discord.Game(name=f"Now playing {song_name}"))
    await update_embed(ctx, song_name, song_url, 0, voice_clients[server_id], song_queues[server_id])

# Volume command
@bot.command()
async def volume(ctx, level: int):
    if not (0 <= level <= 150):
        await ctx.send("Volume must be between 0 and 150.", ephemeral=True)
        return

    server_id = ctx.guild.id
    if server_id not in voice_clients or not voice_clients[server_id].is_connected():
        await ctx.send("No active voice connection.", ephemeral=True)
        return

    current_volumes[server_id] = level / 100
    voice_clients[server_id].source.volume = current_volumes[server_id]
    await ctx.send(f"Volume set to {level}%", ephemeral=True)

# Next command
@bot.command(aliases=["n", "skip"])
async def next(ctx):
    server_id = ctx.guild.id

    if server_id in voice_clients and voice_clients[server_id].is_playing():
        voice_clients[server_id].stop()

    await next_song(ctx)

# Stop command
@bot.command(aliases=["s"])
async def stop(ctx):
    server_id = ctx.guild.id

    if server_id in voice_clients:
        voice_clients[server_id].stop()
        await voice_clients[server_id].disconnect()
        await bot.change_presence(activity=None)
        await ctx.send("Music stopped.")
    else:
        await ctx.send("No active voice connection.")

# Skip to the next song
async def next_song(ctx):
    server_id = ctx.guild.id

    if server_id in song_queues and song_queues[server_id]:
        next_url, next_name = song_queues[server_id].pop(0)
        try:
            source = FFmpegPCMAudio(next_url, **ffmpeg_options)
            source = discord.PCMVolumeTransformer(source, current_volumes.get(server_id, 1.0))
            voice_clients[server_id].play(source, after=lambda e: asyncio.run_coroutine_threadsafe(next_song(ctx), bot.loop))

            await bot.change_presence(activity=discord.Game(name=f"Now playing {next_name}"))
            await update_embed(ctx, next_name, next_url, 0, voice_clients[server_id], song_queues[server_id])
        except Exception as e:
            await ctx.send(f"Error playing the next song: {e}")
    else:
        await ctx.send("Queue is empty. Please add more songs!")
        await bot.change_presence(activity=None)

TOKEN = "<Your Token>"
bot.run(TOKEN)