from src.utils.patterns import Pattern


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
        self.patterns: dict[Pattern] = {}
        self.lexemes: list = []

        # Input pointers
        # Marks the beginning of the current lexeme, whose extent we are attempting to determine.
        self.lexemeBegin: int = 0
        # Scans ahead until a pattern match is found.
        self.forward: int = 0

    def addPattern(self, pattern: Pattern) -> None:
        '''
        This function adds a pattern to the patterns dictionary.
        Parameters:
        - pattern: A pattern object.
        '''
        self.patterns[pattern.name] = pattern

    def buildPatterns(self) -> None:
        '''
        This function builds the DFAs for each pattern in the patterns dictionary.
        '''
        for pattern in self.patterns.values():
            pattern.build()
