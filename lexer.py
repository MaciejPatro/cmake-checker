import ply.lex as lex


class Lexer(object):

    states = (
        ('targetsources', 'exclusive'),
        ('setfunc', 'exclusive'),
        ('disabled', 'exclusive'),
        ('comments', 'exclusive'),
    )

    tokens = ['FILE_GLOB',
              'ADD_COMPILE_OPTIONS',
              'INCLUDE_DIRECTORIES',
              'LINK_DIRECTORIES',
              'LINK_LIBRARIES',
              'COMPILE_FLAGS',
              'CLOSING_COMMAND_WITH_CLAUSE',
              'ADD_DEFINITIONS',
              'ADD_COMPILE_DEFINITIONS',
              'MODIFY_ENV_VARIABLE',
              'CACHE_IN_SET',
              'PARENT_DIR_ACCESS'
              ]

    t_FILE_GLOB = r'file[ \t]*\([ \t]*GLOB'
    t_ADD_COMPILE_OPTIONS = r'add_compile_options[ \t]*\('
    t_ADD_DEFINITIONS = r'add_definitions[ \t]*\('
    t_ADD_COMPILE_DEFINITIONS = r'add_compile_definitions[ \t]*\('
    t_INCLUDE_DIRECTORIES = r'(^include_directories[ \t]*\()|([ \t]+include_directories[ \t]*\()'
    t_LINK_DIRECTORIES = r'(^link_directories[ \t]*\()|([ \t]+link_directories[ \t]*\()'
    t_LINK_LIBRARIES = r'(^link_libraries[ \t]*\()|([ \t]+link_libraries[ \t]*\()'
    t_COMPILE_FLAGS = r'(CMAKE_CXX_FLAGS)|(CMAKE_C_FLAGS)'
    t_CLOSING_COMMAND_WITH_CLAUSE = r'(endif\(.+\))|(endmacro\(.+\))|(endfunction\(.+\))|(endforeach\(.+\))'
    t_setfunc_MODIFY_ENV_VARIABLE = r'[ \t]*ENV\{'
    t_setfunc_CACHE_IN_SET = r'[ \t]+CACHE'
    t_targetsources_PARENT_DIR_ACCESS = r'\.\.\/\.\.'

    def __init__(self):
        self.lexer = lex.lex(module=self)

    @staticmethod
    def t_ANY_error(t: lex.Token) -> None:
        t.lexer.skip(1)

    @staticmethod
    def t_INITIAL_disabled_setfunc_targetsources_newline(t: lex.Token) -> None:
        r"""\n+"""
        t.lexer.lineno += len(t.value)

    @staticmethod
    def t_begin_targetsources(t: lex.Token) -> None:
        r"""[ \t]*target_sources[ \t]*\("""
        t.lexer.push_state('targetsources')

    @staticmethod
    def t_targetsources_end(t: lex.Token) -> None:
        r"""\)"""
        t.lexer.pop_state()

    @staticmethod
    def t_begin_setfunc(t: lex.Token) -> None:
        r"""set[ \t]*\("""
        t.lexer.push_state('setfunc')

    @staticmethod
    def t_setfunc_end(t: lex.Token) -> None:
        r"""\)"""
        t.lexer.pop_state()

    @staticmethod
    def t_comments_begin_disabled(t: lex.Token) -> None:
        r"""cmake-check[ \t]+disable"""
        t.lexer.push_state('disabled')

    @staticmethod
    def t_disabled_end(t: lex.Token) -> None:
        r"""cmake-check[ \t]+enable"""
        t.lexer.pop_state()

    @staticmethod
    def t_INITIAL_targetsources_setfunc_begin_comments(t: lex.Token) -> None:
        r"""([^\\]\#)|.{0}\#"""
        t.lexer.push_state('comments')

    @staticmethod
    def t_comments_end(t: lex.Token) -> None:
        r"""\n+"""
        t.lexer.pop_state()
        t.lexer.lineno += len(t.value)

    def analyze(self, data: str) -> list:
        self.lexer.input(data)
        self.lexer.lineno = 1

        tokens = []

        while True:
            token = self.lexer.token()
            if not token:
                break
            tokens.append(token)

        return tokens
