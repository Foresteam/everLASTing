# https://www.youtube.com/watch?v=c2ZGE5Fpu9E
from xml.etree.ElementTree import ElementTree as ET

class Test:
    def load(self, filename):
        tree = ET.parse(filename)
        
    def __init__(self, filename: str):
        self.load(filename)