from src.utils.patterns import Pattern
from src.utils.structures.symbol import Symbol
from src._expression import Expression


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
        self.codifySourceCode()
        self.patterns: dict = {}
        self.sequences: dict = {}
        self.symbolsTable: list[Symbol] = []

    def addPatterns(self, patterns: list[Pattern]) -> None:
        '''
        This function adds a list of patterns to the patterns dictionary.
        Parameters:
        - patterns: A list of pattern objects.
        '''
        for pattern in patterns:
            self.addPattern(pattern)

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
        for idx, pattern in enumerate(self.patterns.values()):
            pattern.build(idx)

    def codifySourceCode(self):
        '''
        This function codifies the source code.
        '''
        self.expr = Expression(self.sourceCode)
        self.expr.infixRegEx = self.expr.softCodify(
            self.expr.infixRegEx
        )

    def removeSymbols(self, withPatterns: list[Pattern]):
        '''
        This function removes the symbols that are in the withPatterns list.
        Parameters:
        - withPatterns: A list of patterns.
        '''
        self.symbolsTable: list[Symbol] = list(
            filter(lambda symbol: symbol.type not in [pattern.name for pattern in withPatterns],
                   self.symbolsTable)
        )

    def addSequence(self, sequenceID: str, sequence: list):
        '''
        This function adds a sequence to the sequences dictionary.
        Parameters:
        - sequenceID: The id of the sequence.
        - sequence: The sequence to be added.
        '''
        self.sequences[sequenceID] = sequence

    def tokenize(self):
        '''
        This function tokenizes the source code.
        '''
        # This pointer will point to the current character being analyzed.

        forward = 0
        # Strategy:
        # 1. Iterate over the source code.
        # 2. For each character in the source code, check if the current character is a prefix of any pattern.
        # This will be done by sending the entire source code to the DFAs of each pattern.
        # If it is true, then we will get the longest match, and update the lexemeBegin and forward pointers.

        while forward < len(self.expr.infixRegEx):
            longestMatch = None
            for pattern in self.patterns.values():
                _, idx = pattern.min_dir_dfa.simulate(
                    self.expr.infixRegEx[forward:]
                )
                if longestMatch is None:
                    if idx > 0:
                        longestMatch = (pattern.name, idx)
                else:
                    if idx > longestMatch[1]:
                        longestMatch = (pattern.name, idx)
            if longestMatch is not None:
                self.symbolsTable.append(Symbol(
                    longestMatch[0], self.expr.infixRegEx[forward:forward + longestMatch[1]]))
                forward += longestMatch[1]
            else:
                break