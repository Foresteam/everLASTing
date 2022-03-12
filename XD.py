# bot.py
import os
import random
import discord
from discord.ext import commands


DISCORD_TOKEN = 'OTUyMTIyNjMyNzA1MzAyNTc4.YixbTQ.Elvy2SdGST89PFfOySNUXb4yxho'
DISCORD_GUILD = '906579056210899004'
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await message.channel.send('Hello!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send("hallo")
        await message.channel.send(file=discord.File(r'teor/Внешняя изоляция.doc'))
        doc_file_1 = discord.Embed(
            title="ВНЕШНЯЯ ИЗОЛЯЦИЯ",
            url="https://docs.google.com/document/d/13FWtGK5MoJoNWQthVwYF1Fr90UFBdoyj/edit",
            file=discord.File(r'teor/Внешняя изоляция.doc'),
            description="Лекция 2",
            color=discord.Color.blue(),
            )

        doc_file_2 = discord.Embed(
            title="РАЗРЯД ВДОЛЬ ПОВЕРХНОСТИ ТВЕРДОГО ДИЭЛЕКТРИКА",
            url="https://docs.google.com/document/d/1MbzOIKNWgiuKKd-dE-ZIx5Nbv7AhZnqg/edit",
            file=discord.File(r'teor/Внешняя изоляция.doc'),
            description="Лекция 3",
            color=discord.Color.blue(),
        )

        doc_file_3 = discord.Embed(
            title="Учебное пособие",
            url="https://docs.google.com/document/d/1E0e314FPifF9cusxdrcrqJBHUdAT2qc2/edit",
            file=discord.File(r'teor/Внешняя изоляция.doc'),
            description="Все что тебе нужно",
            color=discord.Color.blue(),
        )

        ptt_file_1 = discord.Embed(title="ИЗОЛЯЦИЯ ВОЗДУШНЫХ ЛИНИЙ ЭЛЕКТРОПЕРЕДАЧИ (ВЛЭП) И ОТКРЫТЫХ РАСПРЕДЕЛИТЕЛЬНЫХ УСТРОЙСТВ (ОРУ) ПОДСТАНЦИЙ",
                              url="https://docs.google.com/presentation/d/1CEDW9hArxB_iVJHoWZgZzj7ob4Jwgzxx/edit#slide=id.p1",
                              description="ВНЕШНЯЯ ИЗОЛЯЦИЯ  ЛЭП И ОРУ(призентация)",
                              color=discord.Color.blue(),
                              )
        ptt_file_1.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")

        ptt_file_2 = discord.Embed(title="Повышение электрической прочности внешней изоляции ВЛЭП",
                              url="https://docs.google.com/presentation/d/1CEDW9hArxB_iVJHoWZgZzj7ob4Jwgzxx/edit#slide=id.p1",
                              description="ВЛЭП(призентация)",
                              color=discord.Color.blue(),
                              )
        ptt_file_2.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")

        await message.channel.send(embed=doc_file_1)
        await message.channel.send(embed=doc_file_2)
        await message.channel.send(embed=doc_file_3)
        await message.channel.send(embed=ptt_file_1)
        await message.channel.send(embed=ptt_file_2)



client.run(DISCORD_TOKEN)
