# bot.py
import os
from pathlib import Path
import random
import discord
from discord.ext import commands

import Commander

DISCORD_TOKEN = Path('./token').read_text()
# print(DISCORD_TOKEN)
client = discord.Client()
print('Бот запущен.')
Commander.passClient(client)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    await Commander.onMessage(message)
    return

client.run(DISCORD_TOKEN)
