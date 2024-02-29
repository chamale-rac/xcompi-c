"""
@File name: _expression.py
@Module: Regular Expression
@Author: Samuel Chamalé
@Date: 31/01/2024
@Description: This file contains main algorithms for the regular expression module.
"""


from src.utils.constants import RPAREN, LPAREN, OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR, CONCAT, OPERATORS_PRECEDENCE, TRIVIAL_CHARACTER_PRECEDENCE, LBRACKET, RBRACKET, SINGLE_QUOTE, DOUBLE_QUOTE, RANGE
from src.utils.tools import errorsManager


class Expression(object):
    '''
    This class represents the regular expression module.
    '''

    def __init__(self, infixRegEx: str):
        '''
        This is the constructor of the class.
        Parameters:
        - infixRegEx: A regular expression in infix notation.
        '''
        self.errorsManager = errorsManager()
        self.infixRegEx: str = infixRegEx

    def preprocess(self):
        # Step 1: Codify the regular expression using ascii codes, if operator it maintains the same
        # Step 2: Check parenthesis balance
        # Step 3: Detect group of characters
        self.infixRegEx: list = self.hardCodify(self.infixRegEx)
        if not self.checkBalance():
            self.errorsManager.addError(
                'The regular expression has unbalanced parenthesis', 'Invalid regular expression')
            return

    def process(self):
        self.infixRegExWithCONCAT: str = self.addExplicitConcatenation(
            self.infixRegEx)
        self.postfixRegEx: str = self.shuntingYard(
            self.infixRegExWithCONCAT)

    '''
    ↓↓ ALGORITHMS ↓↓
    '''

    def shuntingYard(self, infixRegEx: str) -> str:
        '''
        Shunting Yard algorithm implementation, it takes a regular expression in infix notation and returns the regular expression in postfix notation.
        Parameters:
        - infixRegEx: A regular expression in infix notation. 
        Returns:
        - A regular expression in postfix notation.
        '''
        postfix = []
        stack = []

        for idx in range(len(infixRegEx)):
            c = infixRegEx[idx]
            if c == LPAREN:
                stack.append(c)
            elif c == RPAREN:
                while stack[-1] != LPAREN:
                    postfix += stack.pop()
                stack.pop()
            else:
                while stack:
                    peekedChar = stack[-1]
                    peekedCharPrecedence = self.getOperatorPrecedence(
                        peekedChar)
                    cPrecedence = self.getOperatorPrecedence(c)
                    if peekedCharPrecedence >= cPrecedence:
                        postfix += stack.pop()
                    else:
                        break
                stack.append(c)

        while stack:
            postfix += stack.pop()
        return postfix

    def addExplicitConcatenation(self, infixRegEx: str) -> str:
        '''
        This function takes a regular expression in infix notation and returns the regular expression with explicit concatenation operators.
        Parameters:
        - infixRegEx: A regular expression in infix notation.
        Returns:
        - A regular expression with explicit concatenation operators.
        '''
        res = []
        lenInfixRegEx = len(infixRegEx)
        for idx in range(lenInfixRegEx):
            c1 = infixRegEx[idx]
            if (idx + 1) < lenInfixRegEx:
                c2 = infixRegEx[idx + 1]
                res += c1

                if c1 not in [LPAREN, OR] and c2 != RPAREN and c2 not in [OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR]:
                    res += CONCAT

        res += infixRegEx[-1]
        return res

    '''
    ↑↑ END ALGORITHMS ↑↑
    '''

    '''
    ↓↓ ASSOCIATED FUNCTIONS ↓↓
    '''

    def getOperatorPrecedence(self, operator): return OPERATORS_PRECEDENCE.get(
        operator, TRIVIAL_CHARACTER_PRECEDENCE)

    def checkBalance(self) -> bool:
        '''
        This function checks if the regular expression has balanced parenthesis, brackets, single quotes and double quotes.
        Returns:
        - True if the regular expression has balanced parenthesis, brackets, single quotes and double quotes, False otherwise.
        '''
        symbols = {LPAREN: 0, LBRACKET: 0,
                   SINGLE_QUOTE: False, DOUBLE_QUOTE: False}
        for c in self.infixRegEx:
            if c in symbols:
                if c in [SINGLE_QUOTE, DOUBLE_QUOTE]:
                    symbols[c] = not symbols[c]  # Toggle quote state
                else:
                    # Increment count for parenthesis or bracket
                    symbols[c] += 1
            elif c in [RPAREN, RBRACKET]:
                if symbols[LPAREN if c == RPAREN else LBRACKET] == 0:
                    return False
                # Decrement count for parenthesis or bracket
                symbols[LPAREN if c == RPAREN else LBRACKET] -= 1
        # Check if all counts are zero and quotes are closed
        return all(not val for val in symbols.values())

    def hardCodify(self, infixRegEx: str) -> list:
        '''
        This function takes a regular expression in infix notation and returns the regular expression codified using ascii codes.
        Parameters:
        - infixRegEx: A regular expression in infix notation.
        Returns:
        - A regular expression codified using ascii codes.
        '''
        result = []
        skip_next = False
        for c in infixRegEx:
            if skip_next:
                result.append(ord(c))
                skip_next = False
            elif c == '\\':
                skip_next = True
            elif c not in [LPAREN, RPAREN, OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR, CONCAT, LBRACKET, RBRACKET, SINGLE_QUOTE, DOUBLE_QUOTE, RANGE]:
                result.append(ord(c))
            else:
                result.append(c)
        return result

    def softCodify(self, infixRegEx: list) -> str:
        '''
        Characters to a list of ASCII codes.
        '''
        return [
            ord(character) for character in infixRegEx
        ]

    def transformGroupsOfCharacters(self, infixRegEx: list) -> list:
        '''
        This function takes a regular expression in infix notation and returns the group of characters in the adequate format.
        Parameters:
        - infixRegEx: A regular expression in infix notation.
        Returns:
        - A list of characters.
        '''
        # TODO: verify that both number are valid intervals, example: a-z, not A-z; or 0-9, not 9-0, or 9-Z
        # TODO: also consider cases when the character isn't inside a quote

        result = []
        idx = 0
        while idx < len(infixRegEx):
            c = infixRegEx[idx]
            if c == LBRACKET:
                idx += 1
                group_result = []
                collected = []

                while infixRegEx[idx] != RBRACKET:
                    if infixRegEx[idx] == SINGLE_QUOTE:
                        # Skip quote
                        idx += 1
                        while infixRegEx[idx] != SINGLE_QUOTE:
                            collected.append(infixRegEx[idx])
                            idx += 1
                    elif infixRegEx[idx] == DOUBLE_QUOTE:
                        # Skip quote
                        idx += 1
                        while infixRegEx[idx] != DOUBLE_QUOTE:
                            collected.append(infixRegEx[idx])
                            idx += 1
                    elif infixRegEx[idx] == RANGE:
                        collected.append(infixRegEx[idx])

                    idx += 1

                for local_idx in range(len(collected)):
                    if collected[local_idx] == RANGE:
                        # Get the previous character in the collected list
                        previous = collected[local_idx - 1]
                        # Get the next character in the collected list
                        next = collected[local_idx + 1]
                        # Add all the characters between the previous and next character
                        # The previous and next are already in ASCII code, so we can use them as integers
                        for i in range(previous, next + 1):
                            group_result.append(i)
                    else:
                        group_result.append(collected[local_idx])

                # Avoid repeating, so cast to set
                result.extend(list(set(group_result)))
            else:
                result.append(c)
            idx += 1

        return result

    '''
    ↑↑ END ASSOCIATED FUNCTIONS ↑↑
    '''


"""
@References: https://gist.github.com/gbrolo/1a80f67f8d0a20d42828fb3fdb7be4de
"""
