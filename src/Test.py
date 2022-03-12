# https://www.youtube.com/watch?v=c2ZGE5Fpu9E
import json
from xml.etree.ElementTree import ElementTree as ET, Element
from discord import Color

class Test:
    class Embedded:
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
                self.color = Color.from_rgb(*map(int, color.replace('rgb', '').replace('(', '').replace(')', '').split(',')))
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    class Msg:
        def __init__(self):
            self.text = ''
            self.attachments: list[str] = []
            self.embedded: list[Test.Embedded] = []
        def fromXML(self, xml: Element):
            for child in xml:
                if child.tag == 'text':
                    self.text += child.text
                if child.tag == 'attachment':
                    self.attachments.append(child.attrib['uri'])
                if child.tag == 'embedded':
                    self.embedded.append(Test.Embedded(child.attrib))
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
            if 'all' in self.levels:
                self.levels = ['easy', 'medium', 'hard']
            for child in xml:
                if child.tag == 'option':
                    self.options.append(Test.Option(child, self.type))
            return self
        def check(self, answer: str) -> float:
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
    def load(self, filename: str):
        xml: Element = ET(file=filename).getroot()
        self.mix = 'mix' in xml.attrib
        self.name = xml.attrib['name']
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
        # for k in self.levels:
        #     for level in self.levels[k]:
        #         print(level.toJSON())
        # print(self.theory.toJSON())

    def __init__(self, filename: str):
        self.load(filename)

Test('test.xml')