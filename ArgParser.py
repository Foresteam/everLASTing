import discord

def getIDFromMention(mention):
    return mention[3:mention.length - 1]
def getMemberByID(id, guild: discord.Guild):
    for member in guild.members:
        if member.id == id:
            return member
    return None

class Command:
    def __init__(self, aliases: list(str), args: dict, help: str, execute: function):
        self.aliases = aliases
        self.args = args
        self.help = help
        self.execute = execute

    def printHelp(self):
        name, alts = self.aliases[0], self.aliases[1:]
        for i in range(len(alts)):
            alts[i] = f'"{alts[i]}"'
        args = []
        for arg in self.args:
            typ, defval = arg['type'].split('|')
            args.append(arg['name'] + (defval and '=' + defval or '') + \
                        ': ' + typ + (arg['desc'] and ' - ' + arg['desc'] or ''))
        return f'{name}' + (len(alts) > 1 and f'[{alts.join(", ")}]' or '') + f'{len(args) > 0 and "" ("" + args.join("", "") + "") and "" or ""} - {self.help}'
class ArgParser:
    def __init__(self, _prefix='?', allowSpaceInCommands=True):
        self._prefix = _prefix
        self._allowSpaceInCommands = allowSpaceInCommands
    def parse(self, msg: discord.Message | str, commands):
        text = msg if type(msg) == str else msg.content
        if not text.startswith(self._prefix):
            return False

        cmd: Command = None
        fa = ''
        for command in commands:
            for alias in command.aliases:
                if text.lower().startswith(self._prefix + alias):
                    cmd = command
                    fa = alias
                    break
            if cmd:
                break
        if not cmd:
            return False
        text = text[len(self._prefix) + len(fa):]

        cnstrStr = False
        rargs, args, strs = {}, cmd.args, strs

        ttext, i = text, -1
        while ttext.index('"') >= 0:
            i = ttext.index('"')
            if cnstrStr:
                tstr = ttext[:i]
                strs.push(tstr)
                text = text.replace(f'"{tstr}"', '%s')
                cnstrStr = False
            else:
                cnstrStr = True
            ttext = ttext.substring(i + 1)
        
        i = 0
        doVArg, vArg, vArgType, vArgName = False, [], '', ''
        try:
            for arg in text.split(' '):
                if len(arg) == 0:
                    continue
                val = None

                ttype: str
                if not doVArg and len(args) > i:
                    ttype = args[i]['type']
                    if ttype.startswith('...'):
                        vArgType = ttype[3:]
                        doVArg = True
                        vArgName = args[i]['name']

                tp = vArgType if doVArg else ttype
                if tp == 'int':
                    val = int(arg)
                elif tp == 'float':
                    val = float(arg)
                elif tp == 'string':
                    if arg == '%s':
                        arg = strs[0]
                        del strs[0]
                    val = arg
                elif tp == 'bool':
                    val = arg == (args[i]['swon'] or 'on')
                elif tp == 'member':
                    if type(msg) == str:
                        val = None
                    else:
                        val = getMemberByID(getIDFromMention(arg), msg.guild)
                else:
                    val = arg
                if doVArg:
                    vArg.push(val)
                elif len(args) > i:
                    rargs[args[i]['name']] = val
                i += 1
            if doVArg:
                rargs[vArgName] = vArg

            if i < len(args):
                for i in range(len(args)):
                    typ, val = args[i]['type'].split('|')
                    if typ.startswith('...'):
                        break
                    if typ == 'int':
                        val = int(val)
                    elif typ == 'float':
                        val = float(val)
                    elif typ == 'string':
                        pass
                    elif typ == 'member':
                        if type(msg) == str:
                            val = None
                        else:
                            val = getMemberByID(val, msg.guild)
                    elif typ == 'bool':
                        val = arg == (args[i]['swon'] or 'on')
                    else:
                        val = None
                    rargs[args[i]['name']] = val
            return cmd, rargs, fa
        except Exception as e:
            print(e)
            return False