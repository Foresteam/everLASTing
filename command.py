# bot.py
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

DISCORD_TOKEN = 'OTUyMTIyNjMyNzA1MzAyNTc4.YixbTQ.vnzgQeRAu95l64Xv5qcEZSd6o14'

bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

@bot.command(name="hello")
async def hello(ctx):
    author = ctx.message.author

    await ctx.send(f'Hello, {author.mention}!')

@bot.command(name="start") # Не передаём аргумент pass_context, так как он был нужен в старых версиях.
async def start(ctx): # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author # Объявляем переменную author и записываем туда информацию об авторе.


    start_embed = discord.Embed(
        title="Добро пожаловать\nПора учиться играя",
        description="С чего начнем",
        color=discord.Color.blue(),
    )



    await ctx.send(embed=start_embed,
                   components=[
                       Button(style=ButtonStyle.green, label="ВНЕШНЯЯ ИЗОЛЯЦИЯ", custom_id="v_1"),
                       Button(style=ButtonStyle.green, label="РАЗРЯД ВДОЛЬ ПОВЕРХНОСТИ ТВЕРДОГО ДИЭЛЕКТРИКА", custom_id="v_2"),
                       Button(style=ButtonStyle.green, label="Учебное пособие", custom_id="v_3"),
                       Button(style=ButtonStyle.green, label="ИЗОЛЯЦИЯ ВОЗДУШНЫХ ЛИНИЙ ЭЛЕКТРОПЕРЕДАЧИ (ВЛЭП)", custom_id="v_4"),
                       Button(style=ButtonStyle.green, label="Повышение электрической прочности внешней изоляции ВЛЭП", custom_id="v_5"),
                   ]
                           )


    while True:
        interaction = await bot.wait_for("button_click")
        if interaction.custom_id == "v_1":
            doc_file_1 = discord.Embed(
                title="ВНЕШНЯЯ ИЗОЛЯЦИЯ",
                url="https://docs.google.com/document/d/13FWtGK5MoJoNWQthVwYF1Fr90UFBdoyj/edit",
                file=discord.File(r'teor/Внешняя изоляция.doc'),
                description="Лекция 2",
                color=discord.Color.blue(),
            )
            await interaction.respond(embed=doc_file_1, ephemeral=True)
        elif interaction.custom_id == "v_2":
            doc_file_2 = discord.Embed(
                title="РАЗРЯД ВДОЛЬ ПОВЕРХНОСТИ ТВЕРДОГО ДИЭЛЕКТРИКА",
                url="https://docs.google.com/document/d/1MbzOIKNWgiuKKd-dE-ZIx5Nbv7AhZnqg/edit",
                description="Лекция 3",
                color=discord.Color.blue(),
            )
            await interaction.respond(embed=doc_file_2, ephemeral=True)
        elif interaction.custom_id == "v_3":
            doc_file_3 = discord.Embed(
                title="Учебное пособие",
                url="https://docs.google.com/document/d/1E0e314FPifF9cusxdrcrqJBHUdAT2qc2/edit",
                file=discord.File(r'teor/Внешняя изоляция.doc'),
                description="Все что тебе нужно",
                color=discord.Color.blue(),
            )
            await interaction.respond(embed=doc_file_3, ephemeral=True)
        elif interaction.custom_id == "v_4":
            ptt_file_1 = discord.Embed(
                title="ИЗОЛЯЦИЯ ВОЗДУШНЫХ ЛИНИЙ ЭЛЕКТРОПЕРЕДАЧИ (ВЛЭП) И ОТКРЫТЫХ РАСПРЕДЕЛИТЕЛЬНЫХ УСТРОЙСТВ (ОРУ) ПОДСТАНЦИЙ",
                url="https://docs.google.com/presentation/d/1CEDW9hArxB_iVJHoWZgZzj7ob4Jwgzxx/edit#slide=id.p1",
                description="ВНЕШНЯЯ ИЗОЛЯЦИЯ  ЛЭП И ОРУ(призентация)",
                color=discord.Color.blue(),
                )
            ptt_file_1.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
            await interaction.respond(embed=ptt_file_1, ephemeral=True)
        elif interaction.custom_id == "v_5":
            ptt_file_2 = discord.Embed(title="Повышение электрической прочности внешней изоляции ВЛЭП",
                                       url="https://docs.google.com/presentation/d/1CEDW9hArxB_iVJHoWZgZzj7ob4Jwgzxx/edit#slide=id.p1",
                                       description="ВЛЭП(призентация)",
                                       color=discord.Color.blue(),
                                       )
            ptt_file_2.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
            await interaction.respond(embed=ptt_file_2, ephemeral=True)



bot.run(DISCORD_TOKEN)
