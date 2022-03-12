import discord
from enum import Enum
from ArgParser import Command, ArgParser

class State(Enum):
    IDLE = 0
    WAITING_FOR_REPLY = 1
class Page(Enum):
    MENU = 0
    GAME = 1

def Help(args, refwith, msg):
    print(args, refwith)

parser = ArgParser()
commands = [
    Command(
        ['help', '?'],
        [ { 'type': 'string', 'name': 'arg' } ],
        '',
        Help
    )
]
cmd: Command
try:
    cmd, args, refwith = parser.parse(input(), commands)
    cmd.execute(args=args, refwith=refwith, msg=None)
except:
    pass