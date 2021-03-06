# https://www.youtube.com/watch?v=c2ZGE5Fpu9E
from copy import deepcopy
from functools import reduce
from posixpath import basename
from random import shuffle
import xml.etree.ElementTree as ET
import discord

def generateMention(id: str):
	return f'<@!{id}>'

class Test:
	class Embed:
		def __init__(self):
			self.url: str
			self.title: str
			self.description: str
			self.thumbnail: str = None
			self.image: str = None
			self.color: int
		def fromXML(self, xml: ET.Element):
			self.url = xml.attrib['url'] if 'url' in xml.attrib else ''
			self.title = xml.attrib['title'] if 'title' in xml.attrib else ''
			self.description = ''
			color = xml.attrib['color'] if 'color' in xml.attrib else '#FFF'
			if color.startswith('#'):
				color = color[1:]
				if len(color) == 3:
					color = ''.join([d + '0' for d in color])
				self.color = int(color, 16)
			else:
				self.color = discord.Color.from_rgb(*map(int, color.replace('rgb', '').replace('(', '').replace(')', '').split(',')))
			for child in xml:
				if child.tag == 'thumbnail':
					self.thumbnail = child.attrib['url'] if 'url' in child.attrib else None
				if child.tag == 'image':
					self.image = child.attrib['url'] if 'url' in child.attrib else None
				if child.tag == 'text':
					self.description += child.text
			return self
	class Msg:
		def __init__(self):
			self.text = ''
			self.attachments: list[str] = []
			self.embed: Test.Embed = None
		def fromXML(self, xml: ET.Element):
			for child in xml:
				if child.tag == 'text':
					self.text += child.text
				if child.tag == 'attachment':
					self.attachments.append(child.attrib['url'])
				if child.tag == 'embed':
					self.embed = Test.Embed().fromXML(child)
			return self
	class Option:
		def __init__(self, xml: ET.Element, typ: str):
			self.correct = 'correct' in xml.attrib
			self.text: str = None
			if typ != 'text':
				self.text = xml.text
			else:
				self.correct = xml.attrib['correct'] if 'correct' in xml.attrib else ''
	class Unit:
		def __init__(self):
			self.beforeSend: list[Test.Msg] = []
			self.msg: Test.Msg = Test.Msg()
		def fromXML(self, xml: ET.Element):
			self.msg = self.msg.fromXML(xml)
			for child in xml:
				if child.tag == 'message':
					self.beforeSend.append(Test.Msg().fromXML(child))
			return self
	class Theory(Unit):
		pass
	class Question(Unit):
		def __init__(self):
			Test.Unit.__init__(self)
			self.type = 'multi-choice'
			self.levels = ['easy', 'medium', 'hard']
			self.options: list[Test.Option] = []
			self.weight = 1
		def fromXML(self, xml: ET.Element):
			Test.Unit.fromXML(self, xml)
			if 'type' in xml.attrib:
				self.type = xml.attrib['type']
			if 'weight' in xml.attrib:
				self.weight = int(xml.attrib['weight'])
			if 'levels' in xml.attrib:
				self.levels = xml.attrib['levels'].split()
			for child in xml:
				if child.tag == 'option':
					self.options.append(Test.Option(child, self.type))
			return self
		def Check(self, answer) -> float:
			if self.type == 'single-choice':
				return self.weight if self.options[int(answer.split()[0]) - 1].correct else 0
			if self.type == 'multi-choice':
				correct = 0
				chosen = [a for a in answer.split()]
				for k, v in [(i, self.options[i],) for i in range(len(self.options))]:
					if str(k + 1) in chosen and v.correct or not v.correct and str(k + 1) not in chosen:
						correct += 1
				return correct / len(self.options) * self.weight
			if self.type == 'text':
				for v in self.options:
					if v.correct and v.correct.lower().replace(' ', '') == answer.lower().replace(' ', ''):
						return self.weight
				return 0
	def Load(self, filename: str):
		print(f'Loading {filename}...')
		xml: ET.Element = ET.parse(filename, parser=ET.XMLParser(encoding='utf-8')).getroot()

		self.mix = 'mix' in xml.attrib
		self.name = basename(filename).replace('.xml', '')
		self.health = int(xml.attrib['health']) if 'health' in xml.attrib else None
		self.theory = Test.Theory()
		self.levels = { 'easy': [], 'medium': [], 'hard': [] }
		for child in xml:
			if child.tag == 'theory':
				self.theory.fromXML(child)
			if child.tag == 'question':
				q: Test.Question = Test.Question().fromXML(child)
				for k in self.levels:
					if k in q.levels:
						self.levels[k].append(q)
		trem = []
		for k in self.levels:
			if len(self.levels[k]) == 0:
				trem.append(k)
		for k in reversed(trem):
			del self.levels[k]

	def __init__(self, filename: str):
		self.progress: int = -1
		self.score: float = 0
		self.level: str
		self.participants: list[str]

		self.Load(filename)

	def GetInstance(self, level: str):
		t = deepcopy(self)
		if t.mix:
			for k in t.levels:
				shuffle(t.levels[k])
		t.level = level
		t.participants = []

		return t
	
	async def __SendMessage(message: discord.Message, channel: discord.TextChannel, msg: Msg, stext = None):
		try:
			e = None
			if msg.embed:
				e = discord.Embed.from_dict(msg.embed.__dict__)
				if msg.embed.image:
					e.set_image(url=msg.embed.image)
				if msg.embed.thumbnail:
					e.set_thumbnail(url=msg.embed.thumbnail)
			await channel.send(
				reference=message,
				files=[discord.File(file) for file in msg.attachments] if len(
					msg.attachments) > 0 else None,
				embed=e,
				content=stext or msg.text
			)
		except Exception as e:
			# await message.reply(str(e))
			raise e
	def GetQuestions(self) -> list[Question]:
		return self.levels[self.level]
	async def Begin(self, message: discord.Message):
		c: discord.TextChannel = message.channel
		for msg in [*self.theory.beforeSend, self.theory.msg]:
			await Test.__SendMessage(message, c, msg)
	def Accept(self, answer: str, message: discord.Message):
		if message.author.id not in self.participants:
			self.participants.append(message.author.id)
		q: Test.Question = self.GetQuestions()[self.progress]
		result = q.Check(answer)
		self.score += result
		if result < q.weight and self.health:
			self.health -= result
			if self.health <= 0:
				return False
		return True
	async def Next(self, message: discord.Message):
		self.progress += 1
		if self.progress >= len(self.GetQuestions()):
			return False
		q: Test.Question = self.GetQuestions()[self.progress]
		msgs = [*q.beforeSend, q.msg]
		opts = []
		for i in range(len(q.options)):
			if q.options[i].text:
				opts.append(f'{i + 1}. {q.options[i].text}')
		for msg in msgs:
			await Test.__SendMessage(message, message.channel, msg, stext=(f'{self.progress + 1}. {msg.text}\n' + '\n'.join(opts) if msg == q.msg else None))
		return True
	def GetTotal(self):
		return reduce(lambda p, v: p + v.weight, self.GetQuestions(), 0)
	async def End(self, message: discord.Message):
		await message.reply(
			f'???????? ??????????????????. ??????????????????: {self.score}/{self.GetTotal()} ({100 * self.score // self.GetTotal()}%)' +
			'\n??????????????????: ' + ', '.join([generateMention(id) for id in self.participants]) +
			f'\n {"<" if len(self.participants) < 2 else "???"}2,  ?????????? **{"" if len(self.participants) < 2 else "????"}????????????**'
		)