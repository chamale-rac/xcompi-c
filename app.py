import argparse


from src._lexer import Lexer
from src.utils.tools import readYalFile, str2bool
from src.utils.patterns import ID, WS, EQ, EXPR, COMMENT, RETURN, LET, OPERATOR, GROUP, RULE, OR, CHAR
from src.utils.constants import IDENT, VALUE, MATCH, EXIST, EXTRACT_REMINDER
from src._yal_seq import YalSequencer as YalSeq
from src.utils.structures.symbol import Symbol
from src._expression import Expression
from src._ast import AbstractSyntaxTree as AST


def main():

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('file_path', type=str, help='The file path')
    parser.add_argument('dir_name', type=str, help='The directory name')
    parser.add_argument('draw_subtrees', type=str2bool,
                        help='A boolean flag to draw the subtrees or not.')

    args = parser.parse_args()

    file_path = args.file_path
    dir_name = args.dir_name
    draw_subtrees = args.draw_subtrees

    fileContent = readYalFile(file_path)

    lexer = Lexer(fileContent)
    lexer.addPatterns([COMMENT, WS, ID, EQ, EXPR, RETURN])
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
    removedAmount = rule_lexer.removeSymbolsByMatch(OR)
    if removedAmount == len(rule_lexer.symbolsTable) - 1:
        print('The rule was removed')
    else:
        # RAISE AN ERROR
        print('Error in definition')

    if draw_subtrees:
        for ident in yal_let.idents.keys():
            this_expression: Expression = Expression(yal_let.idents[ident])
            this_expression.hardProcess()
            this_ast: AST = AST(this_expression.infixRegEx)
            this_ast.draw(ident, dir_name, ident, False)

    final_expression: list = []

    for symbol in rule_lexer.symbolsTable:
        if symbol.type == ID.name:
            final_expression.extend(yal_let.idents[symbol.original])
        else:
            final_expression.extend(symbol.original)
        final_expression.append('|')

    # Remove the last character, cause the last character is a '|'
    final_expression.pop()

    final_expression: Expression = Expression(final_expression)
    final_expression.hardProcess()

    final_ast: AST = AST(final_expression.infixRegEx)
    final_ast.draw('FINAL_AST', dir_name, 'FINAL AST', False)

    final_ast.errorsManager.printErrors('FINAL_AST')


if __name__ == "__main__":
    main()
