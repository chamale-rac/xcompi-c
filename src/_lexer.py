class Lexer(object):
    '''
    This class represents the lexer module.
    '''

    def __init__(self, sourceCode: str):
        '''
        This is the constructor of the class.
        Parameters:
        - sourceCode: The source code to be tokenized.
        '''
        self.sourceCode: str = sourceCode
        self.tokens: list = []
        self.patterns: dict = {}
        self.lexemes: list = []

        # Input pointers
        # Marks the beginning of the current lexeme, whose extent we are attempting to determine.
        self.lexemeBegin: int = 0
        # Scans ahead until a pattern match is found.
        self.forward: int = 0
