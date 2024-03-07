"""
@File name: _expression.py
@Module: Regular Expression
@Author: Samuel Chamalé
@Date: 31/01/2024
@Description: This file contains main algorithms for the regular expression module.
"""
# TODO: consider changing the notation for '' and  "" to be detected as a single character
# TODO: handle when some character is insider '' or "" maybe after detecting groups
# or maybe not cause I can extract them.

from src.utils.constants import RPAREN, LPAREN, OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR, CONCAT, OPERATORS_PRECEDENCE, TRIVIAL_CHARACTER_PRECEDENCE, LBRACKET, RBRACKET, SINGLE_QUOTE, DOUBLE_QUOTE, RANGE
from src.utils.tools import errorsManager


class Expression(object):
    '''
    This class represents the regular expression module.
    '''

    def __init__(self, infixRegEx: str = None):
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
                    postfix += [stack.pop()]
                stack.pop()
            else:
                while stack:
                    peekedChar = stack[-1]
                    peekedCharPrecedence = self.getOperatorPrecedence(
                        peekedChar)
                    cPrecedence = self.getOperatorPrecedence(c)
                    if peekedCharPrecedence >= cPrecedence:
                        postfix += [stack.pop()]
                    else:
                        break
                stack.append(c)

        while stack:
            postfix += [stack.pop()]
        return postfix

    def addExplicitConcatenation(self, infixRegEx: list) -> str:
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
                res += [c1]
                if c1 not in [LPAREN, OR] and c2 != RPAREN and c2 not in [OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR]:
                    res += CONCAT
        res += [infixRegEx[-1]]
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
        for idx, c in enumerate(infixRegEx):
            if skip_next:
                # TODO: Consider special cases as \t, \n and \s
                if c == 'n':
                    result.append(str(ord('\n')))
                elif c == 't':
                    result.append(str(ord('\t')))
                elif c == 's':
                    result.append(str(ord(' ')))
                else:
                    result.append(str(ord(c)))
                skip_next = False
            elif c == '\\':
                skip_next = True
            elif c == ' ':
                # If is inside a quote add as ASCII code, else appends as is
                # Check have previous quote
                if result[-1] in [SINGLE_QUOTE] and infixRegEx[idx+1] in [SINGLE_QUOTE]:
                    result.append(str(ord(c)))
                else:
                    result.append(c)
            elif c == '_':
                print('UNDERSCORE')
                # Number from 0 to 255, with | operator, ex: 0 | 1 | 2 | ... | 255
                for i in range(256):
                    result.append(str(i))
                    if i != 255:
                        result.append(OR)
                print('END UNDERSCORE')
            elif c not in [LPAREN, RPAREN, OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR, CONCAT, LBRACKET, RBRACKET, SINGLE_QUOTE, DOUBLE_QUOTE, RANGE]:
                result.append(str(ord(c)))
            else:
                result.append(c)
        return result

    def softCodify(self, infixRegEx: list) -> str:
        '''
        Characters to a list of ASCII codes.
        '''
        result = []
        for idx, c in enumerate(infixRegEx):
            if c == ' ':
                # If is inside a quote add as ASCII code, else appends as is
                # Check have previous quote
                # TODO:Consider when space is inside a group, ex: "a b"
                if result[-1] in [str(ord(SINGLE_QUOTE))] and infixRegEx[idx+1] in [SINGLE_QUOTE]:
                    result.append(str(ord(c)))
                else:
                    result.append(c)
            else:
                result.append(str(ord(c)))
        return result

    def transformSingleCharacters(self, infixRegEx: list) -> list:
        # TODO transform based on double quotes
        '''
        This function takes a regular expression in infix notation and returns the single characters in the adequate format.
        Parameters:
        - infixRegEx: A regular expression in infix notation.
        Returns:
        - A list of characters.
        '''
        result = []
        idx = 0
        while idx < len(infixRegEx):
            c = infixRegEx[idx]
            if c == SINGLE_QUOTE:
                idx += 1
                while infixRegEx[idx] != SINGLE_QUOTE:
                    result.append(infixRegEx[idx])
                    idx += 1
            else:
                result.append(c)
            idx += 1
        return result

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
                            if infixRegEx[idx] in [RANGE, ONE_OR_MORE]:
                                print('RANGE')
                                collected.append(str(ord(infixRegEx[idx])))
                            else:
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
                        for i in range(int(previous), int(next) + 1):
                            group_result.append(str(i))
                    else:
                        group_result.append(collected[local_idx])

                # Avoid repeating, so cast to set
                group_result = list(set(group_result))

                # Group result need to have a LPAREN at the beginning and a RPAREN at the end
                # Each item needs to be separated by an OR
                # Example [LPAREN, 97, OR, 98, OR, 99, RPAREN]
                group_result.insert(0, LPAREN)
                for i in range(2, len(group_result)*2, 2):
                    group_result.insert(i, OR)
                # Pop the last OR
                group_result.pop()
                group_result.append(RPAREN)

                result.extend(
                    group_result
                )
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
