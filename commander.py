import discord
from enum import Enum
from ArgParser import Command, ArgParser

class State(Enum):
    IDLE = 0
    WAITING_FOR_REPLY = 1
class Page(Enum):
    MENU = 0
    GAME = 1

