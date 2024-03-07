from src._lexer import Lexer
from src.utils.patterns import Pattern
from src.utils.constants import MATCH, EXIST, IDENT, VALUE, EXTRACT_REMINDER
from src.utils.structures.symbol import Symbol
from src.utils.patterns import CHAR


class YalSequencer(object):
    '''
    This class represents the YAL sequencer.
    '''

    def __init__(self, lexer: Lexer, identSequence: list, exprContains: list[Pattern], extract: Pattern):
        '''
        This is the constructor of the class.
        Parameters: 
        - lexer: A lexer object.
        '''
        self.lexer: Lexer = lexer
        self.identSequence: list = identSequence
        self.functions: dict = {
            MATCH: self.match,
            EXIST: self.exist,
            IDENT: self.ident,
            VALUE: self.value,
            EXTRACT_REMINDER: None
        }
        self.idents: dict = {}
        self.exprContains: list[Pattern] = exprContains
        self.currentIdent: str = ""
        self.extract = extract
        self.reminders = []

    def extractIdent(self):
        '''
        This function returns the identifiers in the source code.
        '''
        symbolsPointer: int = 0
        sequencePointer: int = 0

        while symbolsPointer < len(self.lexer.symbolsTable):
            usingFunction: function = self.functions[self.identSequence[sequencePointer][1]]

            if usingFunction is None:
                if self.identSequence[sequencePointer][1] == EXTRACT_REMINDER:
                    # Reminders all the symbols that are after the last symbol that was processed.
                    self.reminders.extend(
                        self.lexer.symbolsTable[symbolsPointer:])

                    # Then break the loop
                    break
                # TODO: Consider adding a EXTRACT_INTERVAL

            functionResult = usingFunction(symbolsPointer, sequencePointer)

            if functionResult:
                sequencePointer += 1
                symbolsPointer += 1
                if sequencePointer >= len(self.identSequence):
                    sequencePointer = 0
            else:
                symbolsPointer += 1
                sequencePointer = 0

    def match(self, symbolsPointer: int, sequencePointer: int) -> bool:
        if not self.exist(symbolsPointer, sequencePointer):
            return False

        symbol: Symbol = self.lexer.symbolsTable[symbolsPointer]
        sequence: Pattern = self.identSequence[sequencePointer][0]

        lexer = Lexer()
        lexer.unCodified = symbol.original
        lexer.codified = symbol.content
        lexer.addPattern(sequence)
        lexer.buildPatterns()
        lexer.tokenize()

        if len(lexer.symbolsTable) == 0:
            return False

        return True

    def ident(self, symbolsPointer: int, sequencePointer: int) -> bool:

        if not self.exist(symbolsPointer, sequencePointer):
            return False

        symbol: Symbol = self.lexer.symbolsTable[symbolsPointer]

        self.idents[symbol.original] = []
        self.currentIdent = symbol.original

        return True

    def value(self, symbolsPointer: int, sequencePointer: int) -> bool:

        if not self.exist(symbolsPointer, sequencePointer):
            return False

        symbol: Symbol = self.lexer.symbolsTable[symbolsPointer]
        value = []

        # TODO: Here I stop, at this point I need to implement the extraction and recognition of EXPR
        lexer = Lexer()
        lexer.unCodified = symbol.original
        lexer.codified = symbol.content
        lexer.addPatterns(self.exprContains)

        lexer.buildPatterns()
        lexer.tokenize(False)

        if len(lexer.symbolsTable) > 0:
            for subSymbol in lexer.symbolsTable:
                if subSymbol.type == self.extract.name:
                    # Get the definition of the symbol, using the identifier. An looking on idents.
                    value.extend(self.idents.get(subSymbol.original, None))
                elif subSymbol.type == CHAR.name:
                    value.append(subSymbol.original[1])
                else:

                    value.extend(subSymbol.original)

        self.idents[self.currentIdent] = value

        return True

    def exist(self, symbolsPointer: int, sequencePointer: int) -> bool:
        pattern: Pattern = self.identSequence[sequencePointer][0]
        symbol: Symbol = self.lexer.symbolsTable[symbolsPointer]

        if pattern.name != symbol.type:
            return False

        return True
