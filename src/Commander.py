from pathlib import Path
import discord
import os
from enum import Enum
from ArgParser import Command, ArgParser
from Test import Test
import DBOperations
from pandas import DataFrame

DBOperations.Init()

class State(Enum):
	MENU = 0
	TEST_SELECTION = 1
	LEVEL_SELECTION = 2
	QUESTION_ANSWER = 3

class Context:
	def __init__(self):
		self.test: Test
		self.state = State.MENU
TCTX = Context()
def GetContext(msg: discord.Message) -> Context:
	# return TCTX # debug
	global contexts
	ctxType: str
	id: str
	if type(msg.channel) == discord.DMChannel:
		ctxType = 'pm'
		id = msg.author.id
	else:
		ctxType = 'group'
		id = msg.channel.id
	if id not in contexts[ctxType]:
		contexts[ctxType][id] = Context()
	return contexts[ctxType][id]
def LevelEng(level: str):
	if level.startswith('ea'):
		return 'easy'
	if level.startswith('me'):
		return 'medium'
	if level.startswith('ha'):
		return 'hard'
	return { 'легкий': 'easy', 'средний': 'medium', 'сложный': 'hard' }[level]

async def Help(msg: discord.Message, args = {}, refwith = None):
	global commands
	fs: str
	if args['command']:
		for com in commands:
			if (com.aliases.find(args['command']) >= 0):
				fs = com.printHelp()
				break
	else:
		r = ['Список команд:'];
		for com in commands:
			r.append(com.printHelp())
		fs = '\n'.join(r)
	await msg.reply(fs or 'Команда не найдена') # msg.reply
async def ListTests(msg: discord.Message, args = {}, refwith = None):
	global tests
	out = [f'{i + 1}. {tests[i].name}' for i in range(len(tests))]
	out.append('Введите номер игры из списка (начав сообщение с префикса "> " или через "ответить")')
	GetContext(msg).state = State.TEST_SELECTION
	await msg.reply('\n'.join(out))
async def ListLevels(msg: discord.Message, args = {}, refwith = None):
	out = ['легкий (easy)', 'средний (medium)', 'сложный (hard)']
	out.append('Введите сложность (начав сообщение с префикса "> " или через "ответить")')
	GetContext(msg).state = State.LEVEL_SELECTION
	await msg.reply('\n'.join(out))
async def Reply(msg: discord.Message, args = {}, refwith = None):
	args['reply'] = ' '.join(args['reply'])
	global client
	# filter replies to us from other messages
	if not refwith and (not msg.reference or (await (await client.fetch_channel(msg.reference.channel_id)).fetch_message(msg.reference.message_id)).author.id != client.user.id):
		return
	ctx = GetContext(msg)
	try:
		global tests
		if ctx.state == State.TEST_SELECTION:
			ctx.test = tests[int(args['reply']) - 1]
			return await ListLevels(msg=msg)
		if ctx.state == State.LEVEL_SELECTION:
			ctx.test = ctx.test.GetInstance(LevelEng(args['reply'].replace(' ', '').lower()))
			ctx.state = State.QUESTION_ANSWER
			await ctx.test.Begin(msg)
			if not await ctx.test.Next(msg):
				raise Exception('Game is empty!')
			return 
		if ctx.state == State.QUESTION_ANSWER:
			if not ctx.test.Accept(args['reply'], msg) or not await ctx.test.Next(msg):
				await ctx.test.End(msg)
				if len(ctx.test.participants) == 1:
					id = str(ctx.test.participants[0])
					user: discord.User = await client.fetch_user(id)
					DBOperations.TestFinished(id, ctx.test.name, ctx.test.level, ctx.test.score, ctx.test.GetTotal(), user.display_name)
	except Exception as e:
		raise e
async def View(msg: discord.Message, args = {}, refwith = None):
	data = DBOperations.GetResultsByNickname(**args)
	out = []
	for user in data:
		t = []
		t.append(user['nickname'] + ':')
		for name, test in user['tests'].items():
			t.append(f'|\t{name}:')
			for nlevel, level in test.items():
				t.append(f'|\t\t{nlevel}: {level["ratio"]}')
		out.append('\n'.join(t))
	await msg.reply('\n'.join(out) or 'Ничего не найдено :(')
async def Export(msg: discord.Message, args = {}, refwith = None):
	data = DBOperations.GetResultsByNickname(**args)
	out = {'User ID': [], 'User nickname': [], 'Level name': [], 'Difficulty level': [], 'Total score': [], 'Got score': [], 'Ratio%': []}
	for user in data:
		for name, test in user['tests'].items():
			for nlevel, level in test.items():
					out['User ID'].append(str(user['id']))
					out['User nickname'].append(user['nickname'])
					out['Level name'].append(name)
					out['Difficulty level'].append(nlevel)
					out['Total score'].append(level['total'])
					out['Got score'].append(level['solved'])
					out['Ratio%'].append(level['ratio'])
	c: discord.TextChannel = msg.channel
	DataFrame(out).to_excel('export.xlsx', sheet_name='sheet1', index=False)
	await c.send(file=discord.File('./export.xlsx'))
		

commands = [
	Command(
		['?помощь', '?help', '??'],
		[ { 'type': '...string', 'name': 'command', 'desc': 'команда, по которой требуется помощь / ничего для показа списка команд' } ],
		'Помощь/список команд',
		Help
	),
	Command(
		['?играть', '?игра', '?>'],
		[],
		'Начать игру',
		ListTests
	),
	Command(
		['?просмотр', '?view'],
		[
			{ 'type': 'string|', 'name': 'nickname', 'desc': 'никнейм пользователя' },
			{ 'type': 'string|', 'name': 'name', 'desc': 'название уровня' },
			{ 'type': 'string|', 'name': 'level', 'desc': 'уровень сложности' }
		],
		'Просмотр результатов пользователя за прохождение уровня. Без параметров = вывод всей БД',
		View
	),
	Command(
		['?экспорт', '?export'],
		[
			{ 'type': 'string|', 'name': 'nickname', 'desc': 'никнейм пользователя' },
			{ 'type': 'string|', 'name': 'name', 'desc': 'название уровня' },
			{ 'type': 'string|', 'name': 'level', 'desc': 'уровень сложности' }
		],
		'Экспорт результатов пользователя за прохождение уровня. Без параметров = вывод всей БД',
		Export
	),
	Command(
		['>', ''],
		[ { 'type': '...string', 'name': 'reply', 'desc': 'ответ' } ],
		'Ответ на вопрос бота.',
		Reply
	)
]

parser = ArgParser('')
tests: list[Test] = [
	Test('games/test/test1.xml'),
]
for file in os.listdir('games/'):
	if file.endswith('.xml'):
		tests.append(Test(f'games/{file}'))
contexts = {
	'pm': {
		# UID: Context
	},
	'group': {
		#serverID/channelID: Context
	}
}
client: discord.Client
async def onMessage(msg: discord.Message):
	cmd: Command
	# try except...
	cmd, args, refwith = parser.parse(msg, commands)
	await cmd.execute(msg, args=args, refwith=refwith)
def passClient(cl):
	global client
	client = cl