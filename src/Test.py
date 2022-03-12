# https://www.youtube.com/watch?v=c2ZGE5Fpu9E
from copy import deepcopy
import json
from posixpath import basename
from pydoc import describe
from random import shuffle
from xml.etree.ElementTree import ElementTree as ET, Element
import discord

class Test:
    class embed:
        def __init__(self, attrs: dict):
            self.uri = attrs['uri'] if 'uri' in attrs else ''
            self.title = attrs['title'] if 'title' in attrs else ''
            self.description = attrs['description'] if 'description' in attrs else ''
            color = attrs['color'] if 'color' in attrs else '#FFF'
            if color.startswith('#'):
                color = color[1:]
                if len(color) == 3:
                    color = ''.join([d + '0' for d in color])
                self.color = int(color, 16)
            else:
                self.color = discord.Color.from_rgb(*map(int, color.replace('rgb', '').replace('(', '').replace(')', '').split(',')))
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    class Msg:
        def __init__(self):
            self.text = ''
            self.attachments: list[str] = []
            self.embed: Test.embed = None
        def fromXML(self, xml: Element):
            for child in xml:
                if child.tag == 'text':
                    self.text += child.text
                if child.tag == 'attachment':
                    self.attachments.append(child.attrib['uri'])
                if child.tag == 'embed':
                    self.embed = Test.embed(child.attrib)
            return self
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    class Option:
        def __init__(self, xml: Element, typ: str):
            self.correct = 'correct' in xml.attrib
            self.text: str
            if typ != 'text':
                self.text = xml.text
            else:
                self.correct = xml.attrib['correct'] if 'correct' in xml.attrib else ''
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    class Unit:
        def __init__(self):
            self.beforeSend: list[Test.Msg] = []
            self.msg: Test.Msg = Test.Msg()
        def fromXML(self, xml: Element):
            self.msg = self.msg.fromXML(xml)
            for child in xml:
                if child.tag == 'message':
                    self.beforeSend.append(Test.Msg().fromXML(child))
            return self
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    class Theory(Unit):
        pass
    class Question(Unit):
        def __init__(self):
            Test.Unit.__init__(self)
            self.type = 'multi-choice'
            self.levels = ['easy', 'medium', 'hard']
            self.options: list[Test.Option] = []
        def fromXML(self, xml: Element):
            Test.Unit.fromXML(self, xml)
            if 'type' in xml.attrib:
                self.type = xml.attrib['type']
            if 'levels' in xml.attrib:
                self.levels = xml.attrib['levels'].split()
            else:
                self.levels = 'medium'
            if 'all' in self.levels:
                self.levels = ['easy', 'medium', 'hard']
            for child in xml:
                if child.tag == 'option':
                    self.options.append(Test.Option(child, self.type))
            return self
        def Check(self, answer: str) -> float:
            if self.type == 'single-choice':
                return 1 if self.options[int(answer)].correct else 0
            if self.type == 'multi-choice':
                corrent = 0
                chosen = answer.split()
                for k, v in [(i, self.options[i],) for i in range(len(self.options))]:
                    if str(k) in chosen and v.correct or not v.correct:
                        correct += 1
                return len(self.options) / correct
            if self.type == 'text':
                for v in self.options:
                    if v.correct and v.correct.lower().replace(' ', '') == answer.lower().replace(' ', ''):
                        return 1
                return 0
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    def Load(self, filename: str):
        xml: Element = ET(file=filename).getroot()
        self.mix = 'mix' in xml.attrib
        self.name = basename(filename).replace('.xml', '')
        self.passOnError = 'pass-on-error' in xml.attrib
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
        for k in self.levels:
            if len(self.levels[k]) == 0:
                del self.levels[k]
        # for k in self.levels:
        #     for level in self.levels[k]:
        #         print(level.toJSON())
        # print(self.theory.toJSON())

    def __init__(self, filename: str):
        self.progress: int = -1
        self.score: float = 0
        self.level: str

        self.Load(filename)

    def GetInstance(self, level: str):
        t = deepcopy(self)
        if t.mix:
            for k in t.levels:
                shuffle(t.levels[k])
        t.level = level

        return t
    
    async def __SendMessage(message: discord.Message, channel: discord.TextChannel, msg: Msg):
        await channel.send(
            reference=message,
            files=[discord.File(file) for file in msg.attachments] if len(
                msg.attachments) > 0 else None,
            embed=discord.Embed(
                title=msg.embed.title,
                color=msg.embed.color,
                description=msg.embed.description,
                url=msg.embed.uri
            ) if msg.embed else None,
            content=msg.text
        )
    def GetQuestions(self):
        return self.levels[self.level]
    async def Begin(self, message: discord.Message):
        c: discord.TextChannel = message.channel
        for msg in [*self.theory.beforeSend, self.theory.msg]:
            await Test.__SendMessage(message, c, msg)
    def Accept(self, answer: str):
        result = self.GetQuestions()[self.progress].Check(answer)
        self.score += result
        if result < 1 and not self.passOnError:
            return False
        return True
    async def Next(self, message: discord.Message):
        self.progress += 1
        if self.progress >= len(self.GetQuestions()):
            return False
        return True
    async def End(self, message: discord.Message):
        pass