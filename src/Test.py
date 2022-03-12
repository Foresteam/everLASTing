# https://www.youtube.com/watch?v=c2ZGE5Fpu9E
from xml.etree.ElementTree import ElementTree as ET, Element
from discord import Color

class Test:
    class Embedded:
        def __init__(self, uri = '', title = '', description = '', color = '#FFF'):
            self.uri = uri
            self.title = title
            self.description = description
            if color.startswith('#'):
                color = color[1:]
                if len(color) == 3:
                    color = ''.join([d + '0' for d in color])
                color = int(color, 16)
            else:
                color = Color.from_rgb(*map(int, color.replace('rgb', '').replace('(', '').replace(')', '').split(',')))
    class Msg:
        def __init__(self, text: str = '', attachments: list[str] = [], embeddeds = []):
            self.text = text
            self.attachments = attachments
            self.embeddeds: list[Test.Embedded] = embeddeds
    class Unit:
        def __init__(self, beforeSend, msg):
            self.beforeSend: list[Test.Msg] = beforeSend or []
            self.msg: Test.Msg = msg or Test.Msg()
    def load(self, filename: str):
        xml: Element = ET(file=filename).getroot()
        self.mix = 'mix' in xml.attrib
        self.name = xml.attrib['name']
        self.theory = { 'beforeSend': [], 'self': Test.Msg() }


    def __init__(self, filename: str):
        self.load(filename)

Test('test.xml')