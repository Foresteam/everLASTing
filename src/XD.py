# bot.py
from pathlib import Path
import discord

import Commander

DISCORD_TOKEN = Path('./token').read_text()
client = discord.Client()
print('Бот запущен.')
Commander.PassClient(client) # commander init

@client.event
async def on_message(message: discord.Message): # main event
    if message.author == client.user:
        return
    await Commander.OnMessage(message)
    return

client.run(DISCORD_TOKEN) # start bot