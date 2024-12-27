# embed_handler.py
import discord
from discord.ui import View, Button
from datetime import timedelta
import asyncio

# Update the embed
async def update_embed(ctx, song_name, song_url, elapsed_time, voice_client, song_queue):
    # Format elapsed time as HH:MM:SS
    elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))
    embed = discord.Embed(
        title="Now Playing",
        description=f"[**{song_name}**]({song_url})",  # Clickable song link
        color=discord.Color.blue()
    )
    embed.add_field(name="Elapsed Time", value=elapsed_time_str, inline=False)
    embed.set_footer(text="Music Bot | Enjoy the music!")

    # If an embed already exists, edit it; otherwise, send a new one
    if hasattr(ctx, 'embed_message') and ctx.embed_message is not None:
        await ctx.embed_message.edit(embed=embed, view=MusicButtons(ctx, voice_client, song_queue))
    else:
        ctx.embed_message = await ctx.channel.send(embed=embed, view=MusicButtons(ctx, voice_client, song_queue))

    # Periodically update the elapsed time in the embed
    while voice_client.is_playing():
        await asyncio.sleep(5)
        elapsed_time += 5
        elapsed_time_str = str(timedelta(seconds=int(elapsed_time)))
        embed.set_field_at(0, name="Elapsed Time", value=elapsed_time_str)
        await ctx.embed_message.edit(embed=embed)

# Music control buttons
class MusicButtons(View):
    def __init__(self, ctx, voice_client, song_queue):
        super().__init__(timeout=None)  # Keep the view active indefinitely
        self.ctx = ctx
        self.voice_client = voice_client
        self.song_queue = song_queue

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.blurple)
    async def pause_button(self, interaction: discord.Interaction, button: Button):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            await interaction.response.send_message("Music paused.", ephemeral=True)
        else:
            await interaction.response.send_message("No music is playing.", ephemeral=True)

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.green)
    async def resume_button(self, interaction: discord.Interaction, button: Button):
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            await interaction.response.send_message("Music resumed.", ephemeral=True)
        else:
            await interaction.response.send_message("No music is paused.", ephemeral=True)

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: Button):
        if self.voice_client:
            self.voice_client.stop()
            await self.voice_client.disconnect()
            self.ctx.embed_message = None  # Clear the embed message
            await interaction.response.send_message("Music stopped.", ephemeral=True)
        else:
            await interaction.response.send_message("No active voice connection.", ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next_button(self, interaction: discord.Interaction, button: Button):
        if self.song_queue:
            self.voice_client.stop()  # Stop the current song
            next_song_url, next_song_name = self.song_queue.pop(0)
            source = discord.FFmpegPCMAudio(next_song_url)
            self.voice_client.play(source)
            await update_embed(self.ctx, next_song_name, next_song_url, 0, self.voice_client, self.song_queue)
            await interaction.response.defer()  # Avoid "interaction failed" by deferring the response
        else:
            await interaction.response.send_message("No next song in the queue.", ephemeral=True)
