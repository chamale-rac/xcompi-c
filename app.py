from src._lexer import Lexer
from src.utils.tools import readYalFile
from src.utils.patterns import ID, WS, EQ, EXPR, COMMENT, RETURN, LET, OPERATOR, GROUP, RULE, OR, CHAR
from src.utils.constants import IDENT, VALUE, MATCH, EXIST, EXTRACT_REMINDER
from src._yal_seq import YalSequencer as YalSeq
from src.utils.structures.symbol import Symbol
from src._expression import Expression
from src._ast import AbstractSyntaxTree as AST


def main():
    file = input("Enter the file name: ")
    useId = input("Enter the id to use: ")
    useId = int(useId)

    fileContent = readYalFile(file)

    lexer = Lexer(fileContent)
    lexer.addPatterns([COMMENT, WS, ID, EQ, EXPR, RETURN])
    lexer.buildPatterns()
    lexer.tokenize()
    lexer.removeSymbols([COMMENT, RETURN])

    yal_let = YalSeq(
        lexer,
        [
            [LET, MATCH],
            [WS, EXIST],
            [ID, IDENT],
            [WS, EXIST],
            [EQ, EXIST],
            [WS, EXIST],
            [EXPR, VALUE],
        ],
        [ID, OPERATOR, GROUP, CHAR],
        ID
    )

    yal_let.extractIdent()

    yal_rule = YalSeq(
        lexer,
        [
            [RULE, MATCH],
            [WS, EXIST],
            [ID, IDENT],
            [WS, EXIST],
            [EQ, EXIST],
            [None, EXTRACT_REMINDER]
        ],
        None,
        None
    )

    yal_rule.extractIdent()

    rule_lexer = Lexer()
    rule_lexer.symbolsTable = yal_rule.reminders
    rule_lexer.removeSymbols([WS])
    rule_lexer.removeSymbolsByMatch(OR)
    # removedAmount = rule_lexer.removeSymbolsByMatch(OR)
    # if removedAmount - 1 == len(rule_lexer.symbolsTable):
    #     print('The rule was removed')
    # else:
    #     # RAISE AN ERROR
    #     print('Error in definition')

    for ident in yal_let.idents.keys():
        thisExpression: Expression = Expression(yal_let.idents[ident])
        thisExpression.infixRegEx = thisExpression.hardCodify(
            thisExpression.infixRegEx
        )
        thisExpression.infixRegEx = thisExpression.transformGroupsOfCharacters(
            thisExpression.infixRegEx
        )
        thisExpression.infixRegEx = thisExpression.addExplicitConcatenation(
            thisExpression.infixRegEx
        )
        thisExpression.infixRegEx = thisExpression.shuntingYard(
            thisExpression.infixRegEx
        )
        thisAST: AST = AST(thisExpression.infixRegEx)
        thisAST.draw(ident, useId, ident, False)

    finalExpression: list = []

    for symbol in rule_lexer.symbolsTable:
        symbol: Symbol = symbol

        if symbol.type == ID.name:
            finalExpression.append('(')
            finalExpression.extend(yal_let.idents[symbol.original])
            finalExpression.append(')')
        else:
            finalExpression.extend([
                '\\', symbol.original[1]
            ])
        finalExpression.append('|')

    # Remove the last two characters
    finalExpression.pop()

    finalExpression: Expression = Expression(finalExpression)
    finalExpression.infixRegEx = finalExpression.hardCodify(
        finalExpression.infixRegEx
    )
    finalExpression.infixRegEx = finalExpression.transformGroupsOfCharacters(
        finalExpression.infixRegEx
    )

    finalExpression.infixRegEx = finalExpression.addExplicitConcatenation(
        finalExpression.infixRegEx
    )

    finalExpression.infixRegEx = finalExpression.shuntingYard(
        finalExpression.infixRegEx
    )

    finalAST: AST = AST(finalExpression.infixRegEx)
    finalAST.draw('FINAL_AST', useId, 'FINAL AST', False)

    finalAST.errorsManager.printErrors('FINAL_AST')


if __name__ == "__main__":
    main()
