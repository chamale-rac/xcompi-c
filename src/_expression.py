"""
@File name: _expression.py
@Module: Regular Expression
@Author: Samuel Chamalé
@Date: 31/01/2024
@Description: This file contains main algorithms for the regular expression module.
"""


from src.utils.constants import RPAREN, LPAREN, OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR, CONCAT, OPERATORS_PRECEDENCE, TRIVIAL_CHARACTER_PRECEDENCE, LBRACKET, RBRACKET
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
        self.process()

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

    def checkParenthesisBalance(self) -> bool:
        '''
        This function checks if the regular expression has balanced parenthesis and brackets.
        Returns:
        - True if the regular expression has balanced parenthesis and brackets, False otherwise.
        '''
        stack = []
        for c in self.infixRegEx:
            if c in [LPAREN, LBRACKET]:
                stack.append(c)
            elif c in [RPAREN, RBRACKET]:
                if not stack or (c == RPAREN and stack[-1] != LPAREN) or (c == RBRACKET and stack[-1] != LBRACKET):
                    return False
                stack.pop()
        return not stack

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
                result.append(str(ord(c)))
                skip_next = False
            elif c == '\\':
                skip_next = True
            elif c not in [LPAREN, RPAREN, OR, ZERO_OR_ONE, ONE_OR_MORE, KLEENE_STAR, CONCAT, LBRACKET, RBRACKET]:
                result.append(str(ord(c)))
            else:
                result.append(c)
        return result

    '''
    ↑↑ END ASSOCIATED FUNCTIONS ↑↑
    '''


"""
@References: https://gist.github.com/gbrolo/1a80f67f8d0a20d42828fb3fdb7be4de
"""
