from pygments.lexer import RegexLexer, include, bygroups
# from pygments.filters import VisibleWhitespaceFilter
from pygments.token import *

class CustomLexer(RegexLexer):
# class StationeersMIPSLexer(RegexLexer):
    name = 'Stationeers MIPS'
    aliases = ['mips']
    filenames = ['*.mips']

    def whole_words(words):
        for w in words:
            yield r'\b'+w+r'\b'

    instructions = [
        # Device IO
        'bdns', 'bdnsal', 'bdse', 'bdseal', 'brdns', 'brdse', 'l', 'lb', 'lr', 'ls', 's', 'sb',
        # Flow Control, Branches and Jumps
        'bap', 'bapal', 'bapz', 'bapzal', 'beq', 'beqal', 'beqz', 'beqzal', 'bge', 'bgeal', 'bgez',
        'bgezal', 'bgt', 'bgtal', 'bgtz', 'bgtzal', 'ble', 'bleal', 'blez', 'blezal', 'blt',
        'bltal', 'bltz', 'bltzal', 'bna', 'bnaal', 'bnaz', 'bnazal', 'bne', 'bneal', 'bnez',
        'bnezal', 'brap', 'brapz', 'breq', 'breqz', 'brge', 'brgez', 'brgt', 'brgtz', 'brle',
        'brlez', 'brlt', 'brltz', 'brna', 'brnaz', 'brne', 'brnez', 'j', 'jal', 'jr',
        # Variable Selection
        'sap', 'sapz', 'sdns', 'sdse', 'select', 'seq', 'seqz', 'sge', 'sgez', 'sgt', 'sgtz', 'sle',
        'slez', 'slt', 'sltz', 'sna', 'snaz', 'sne', 'snez',
        # Mathematical Operations
        'abs', 'acos', 'add', 'asin', 'atan', 'ceil', 'cos', 'div', 'exp', 'floor', 'log', 'max',
        'min', 'mod', 'mul', 'rand', 'round', 'sin', 'sqrt', 'sub', 'tan', 'trunc',
        # Logic
        'and', 'nor', 'or', 'xor',
        # Stack
        'peek', 'pop', 'push',
        # Misc
        # 'alias',
        # 'define',
        'hcf', 'move', 'sleep', 'yield'
    ]
    instruction = '|'.join(whole_words(instructions))

    parameters = [
        'Quantity',
    ]
    parameter = '|'.join(whole_words(parameters))

    NUM_DEVICES = 6
    device = r'\bdr*(' + '|'.join(str(i) for i in range(NUM_DEVICES)) + r')\b'

    NUM_REGISTERS = 16
    registers = ['sp', 'ra', 'rr*(' + '|'.join(str(i) for i in range(16)) + ')']
    register = '|'.join(whole_words(registers))

    number = r'[+-]?(\d*\.)?\d+'

    tokens = {
        'root': [
            include('whitespace'),
            (r'\w+:', Name.Label),
            ('alias', Keyword.Declaration),
            ('define', Keyword.Declaration),
            (instruction, Keyword),
            (parameter, Keyword.Constant),
            (device, Name.Class),
            (register, Name.Class),
            (number, Number),
            (r'\w+', Text),
        ],
        'whitespace': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),
            (r'([;#]|//).*?\n', Comment.Single),
            (r'/[*][\w\W]*?[*]/', Comment.Multiline),
        ]
    }

