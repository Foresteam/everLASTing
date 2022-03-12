# https://www.youtube.com/watch?v=c2ZGE5Fpu9E
from xml.etree.ElementTree import ElementTree as ET, Element

class Test:
    class Msg:
        def __init__(self, text: str = '', attachments: list[str] = [], embeddeds: list[str] = []):
            self.text = text
            self.attachments = attachments
            self.embeddeds = embeddeds
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