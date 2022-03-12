import discord
from enum import Enum
from ArgParser import Command, ArgParser

class State(Enum):
    IDLE = 0
    WAITING_FOR_REPLY = 1
class Page(Enum):
    MENU = 0
    GAME = 1

def Help(args: list, refwith: str, msg: discord.Message):
    global commands
    fs = ''
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
    print('\n' + (fs or 'Команда не найдена')) # msg.reply
def Reply(args: list, refwith: str, msg: discord.Message):
    return


commands = [
    Command(
        ['?help', '??', '?помощь'],
        [ { 'type': 'string...', 'name': 'command', 'desc': 'команда, по которой требуется помощь / ничего для показа списка команд' } ],
        'Помощь/список команд',
        Help
    ),
    Command(
        ['>', '?>'],
        [ { 'type': 'string...', 'name': 'reply', 'desc': 'ответ' } ],
        'Ответ на вопрос бота.',
        Reply
    )
]
class Commander:
    def __init__(self):
        self.parser = ArgParser('')
        self.contexts = {
            'pm': {
                # UID: Context
            },
            'serversChannels': {
                #serverID/channelID: Context
            }
        }
    def onMessage(self, msg: discord.Message):
        cmd: Command
        # try except...
        cmd, args, refwith = self.parser.parse(input(), commands)
        cmd.execute(args=args, refwith=refwith, msg=None)