# This bot is no longer working as youtube changed its guidelines and we appreciate it.

### Discord-musicbot
A Discord Music Bot made my Me and my Partner Saksham Gupta in python. You Can Edit the code as you like just don't misuse it.

This is a simple Discord music bot that allows users to play music, adjust volume, skip tracks, and more. The bot uses `discord.py` for interacting with Discord, `yt-dlp` for fetching music from YouTube, and SQLite for storing server-specific data.

## Features

- **Play Music**: Play music from YouTube by providing a search query.
- **Volume Control**: Adjust the volume of the bot's audio.
- **Queue System**: Add songs to a queue and skip to the next song.
- **Stop Music**: Stop the current song and disconnect from the voice channel.
- **Server-Specific Settings**: Stores server-specific data, like the channel ID.

## Requirements

To run the bot, you need to install the following dependencies:

1. **Python 3.8+** (Recommended: Python 3.8 or higher)
2. **Discord Bot Token** (See [Getting Your Token](#getting-your-token) section below)
3. **Required Python Libraries**: Use the `requirements.txt` file to install the necessary libraries.

## Installation

### Step 1: Clone the repository

If you haven't cloned the repository yet, do so by running the following command:

```bash
git clone <repository_url>
cd <repository_name>
```

### Step 2: Install Dependencies

Make sure you have `pip` installed, then run the following command to install all the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

This will install the necessary libraries such as `discord.py` and `yt-dlp`.

- You Will Also need ffmpeg installed in your native system to make this run. 

### Step 3: Configure the Bot Token

You need to provide your Discord bot token to authenticate your bot. 

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Select your application and navigate to the **Bot** section.
3. Copy your **Bot Token**.

Now, replace the `TOKEN` variable in the `bot.py` file with your token:

```python
TOKEN = "YOUR_DISCORD_BOT_TOKEN"
```

### Step 4: Run the Bot

After configuring the token, you can start the bot by running:

```bash
python bot.py
```

Your bot should now be running and available to use in your Discord server.

## Bot Commands

Here are the main commands that you can use with the bot:

- **`!play <song_name>`** (Aliases: `!p`): Play a song from YouTube. The bot will search for the song and start playing it in the voice channel.
- **`!volume <level>`**: Set the volume of the bot. The level should be between 0 and 150.
- **`!next`** (Aliases: `!n`, `!skip`): Skip to the next song in the queue.
- **`!stop`** (Aliases: `!s`): Stop the music and disconnect the bot from the voice channel.

## Features

- **Queueing**: If a song is already playing, the bot will add the next song to the queue.
- **Volume Adjustment**: Control the playback volume for better listening experience.
- **Error Handling**: If the bot fails to play a song or connects to the voice channel, it will notify you.

## Troubleshooting

1. **Bot not responding**: Ensure the bot is added to a server and has the necessary permissions to connect and speak in voice channels.
2. **Bot cannot join the voice channel**: Make sure the bot has the `CONNECT` and `SPEAK` permissions for the voice channel.

## License

This project is licensed under the MIT License.

## Credits

- [discord.py documentation](https://discordpy.readthedocs.io/en/stable/)
- [yt-dlp GitHub repository](https://github.com/yt-dlp/yt-dlp)
