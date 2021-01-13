from pygments.lexer import RegexLexer, include, bygroups
# from pygments.filters import VisibleWhitespaceFilter
from pygments.token import *

class CustomLexer(RegexLexer):
# class StationeersMIPSLexer(RegexLexer):
    name = 'Stationeers MIPS'
    aliases = ['mips']
    filenames = ['*.mips']

    keywords = [
        'alias',
        'define',
    ]
    keyword_pattern = '|'.join(keywords)

    identifier = r'(\w+)'


    instructions = [
        'alias',
        'define',
        'move',
    ]

    instruction = '|'.join(instructions)
    device = r'\bdr*(?:'+'|'.join(str(i) for i in range(16))+r')\b'
    register = r'\brr*(?:'+'|'.join(str(i) for i in range(16))+r')\b'
    number = r'[+-]?(\d*\.)?\d+'

    labels = []
    devices = [] # device aliases
    registers = [] # device registers

    def add_alias(lexer, match):
        alias = match.group(1)
        builtin = match.group(3)
        tag = None
        if builtin.startswith('d'):
            lexer.devices += [alias]
            tag = Name.Class
        else:
            lexer.registers += [alias]
            tag = Name.Variable
        yield 0, tag, alias
        yield 1, Whitespace, match.group(2)
        yield 2, tag, builtin

    def add_definition(lexer, match):
        definition = math.group(2)
        value = match.group(4)
        yield 0, Name.Constant, definition
        yield 1, Whitespace, match.group(3)
        yield 2, tag, builtin

    tokens = {
        'root': [
            include('whitespace'),
            (r'\w+:', Name.Label),
            (instruction, Keyword),
            (device, Name.Class),
            (register, Name.Class),
            (number, Number),
            (r'\w', Name),
            # (r'alias', Keyword, 'alias'),
            # (r'define', Keyword, 'define'),
            # (r'(alias)(\s*)(\w+)(\s*)(\b[dr]r*\d\b)', bygroups(Keyword, Whitespace, Name, Whitespace, Number)),
            # (r'(alias)(\s)(\w+)(\s)('+device+')', bygroups(Keyword, Whitespace, Name, Whitespace, Number)),
            # (instruction, Keyword),
            # (device, Name.Class),
            # (register, Name.Variable),
        ],
        'instruction': [
            include('whitespace')
        ],
        'alias': [
            include('whitespace'),
            # (r'(\w+)(\s*)('+var+')', add_alias),
        ],
        'define': [
            include('whitespace'),
            (r'(\w+)(\s*)('+number+')', add_definition),
        ],
        'device': [
        ],
        'register': [
        ],
        'whitespace': [
            (r'\n', Whitespace),
            (r'\s+', Whitespace),
            (r'([;#]|//).*?\n', Comment.Single),
            (r'/[*][\w\W]*?[*]/', Comment.Multiline),
        ]
    }
