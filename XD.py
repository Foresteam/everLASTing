# bot.py
import os
import random
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

DISCORD_TOKEN = 'OTUyMTIyNjMyNzA1MzAyNTc4.YixbTQ.e6ab4XkT77c3UR7mYtV6Uurs_2w'
DISCORD_GUILD = '906579056210899004'
# client = discord.Client()
client = commands.Bot(command_prefix='$')


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

    if message.content == '99!':
        await message.channel.send("hallo")
        await message.channel.send(file=discord.File(r'teor/Внешняя изоляция.doc'))
        doc_file_1 = discord.Embed(
            title="ВНЕШНЯЯ ИЗОЛЯЦИЯ",
            url="https://docs.google.com/document/d/13FWtGK5MoJoNWQthVwYF1Fr90UFBdoyj/edit",

            description="Лекция 2",
            color=discord.Color.blue(),
            )

        doc_file_2 = discord.Embed(
            title="РАЗРЯД ВДОЛЬ ПОВЕРХНОСТИ ТВЕРДОГО ДИЭЛЕКТРИКА",
            url="https://docs.google.com/document/d/1MbzOIKNWgiuKKd-dE-ZIx5Nbv7AhZnqg/edit",

            description="Лекция 3",
            color=discord.Color.blue(),
        )

        doc_file_3 = discord.Embed(
            title="Учебное пособие",
            url="https://docs.google.com/document/d/1E0e314FPifF9cusxdrcrqJBHUdAT2qc2/edit",

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

        await message.channel.send(embed=doc_file_1,
                                   omponents=[
                                       Button(style=ButtonStyle.green, label="Accept", emoji="🎄"),
                                       Button(style=ButtonStyle.red, label="Decline", emoji="🧨"),
                                       Button(style=ButtonStyle.URL, label="test", url="https://www.google.com")
                                   ]
                                   )
        # response = await client.wait_for("button_click")
        # if response.channel == message.channel:
        #     if response.component.label == "text1":
        #         await response.respond(content="Great!")
        #     else:
        #         await response.respond(
        #             embed=discord.Embed(title="Are you sure?"),
        #             components=[
        #                 Button(style=ButtonStyle.green, label="Yes"),
        #                 Button(style=ButtonStyle.red, label="No"),
        #                 Button(style=ButtonStyle.blue, label="I'll think...", emoji="🙄"),
        #
        #             ]
        #         )

        await message.channel.send(embed=doc_file_1)
        await message.channel.send(embed=doc_file_2)
        await message.channel.send(embed=doc_file_3)
        await message.channel.send(embed=ptt_file_1)
        await message.channel.send(embed=ptt_file_2)


@client.command()
async def start(ctx):
    start_embed = discord.Embed(
        title="Добро пожаловать\nПора учиться играя",
        description="С чего начнем",
        color=discord.Color.blue(),
        )
    await ctx.channel.send(embed=start_embed,
                           omponents=[
                               Button(style=ButtonStyle.green, label="ВНЕШНЯЯ ИЗОЛЯЦИЯ", emoji="🎄"),
                               Button(style=ButtonStyle.red, label="РАЗРЯД ВДОЛЬ ПОВЕРХНОСТИ ТВЕРДОГО ДИЭЛЕКТРИКА", emoji="🧨"),
                               Button(style=ButtonStyle.blue, label="Учебное пособие", emoji="🎄")
                           ]
                           )

    response = await client.wait_for("button_click")
    if response.channel == ctx.channel:
        if response.component.label == "text1":
            await response.respond(content="Great!")
        else:
            await response.respond(
                embed=discord.Embed(title="Are you sure?"),
                components=[
                    Button(style=ButtonStyle.green, label="Yes"),
                    Button(style=ButtonStyle.red, label="No"),
                    Button(style=ButtonStyle.blue, label="I'll think...", emoji="🙄"),

                ]
            )


client.run(DISCORD_TOKEN)
