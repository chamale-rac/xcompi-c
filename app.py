import argparse


from src._tokenizer import Tokenizer
from src.utils.tools import readYalFile, str2bool, str2file
from src.utils.patterns import ID, WS, EQ, EXPR, COMMENT, RETURN, LET, OPERATOR, GROUP, RULE, OR, CHAR
from src.utils.constants import IDENT, VALUE, MATCH, EXIST, EXTRACT_REMINDER
from src._yal_seq import YalSequencer as YalSeq
from src._expression import Expression
from src._ast import AbstractSyntaxTree as AST


def main():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('file_path', type=str2file, help='The file path')
    parser.add_argument('dir_name', type=str, help='The directory name')
    parser.add_argument('draw_subtrees', type=str2bool,
                        help='A boolean flag to draw the subtrees or not.')

    args = parser.parse_args()

    file_path = args.file_path
    dir_name = args.dir_name
    draw_subtrees = args.draw_subtrees

    fileContent = readYalFile(file_path)
    print(f'✔ File read successfully from {file_path}')

    lexer = Tokenizer(fileContent)
    lexer.addPatterns([COMMENT, WS, ID, EQ, EXPR, RETURN])
    lexer.tokenize()

    if lexer.errorsManager.haveErrors():
        lexer.errorsManager.printErrors(
            '✖ Tokens has not been generated successfully')
        return

    print('✔ Tokens has been generated successfully:')
    for idx, symbol in enumerate(lexer.symbolsTable):
        print(f'\t[{idx}] {symbol}')

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
    if yal_let.errorsManager.haveErrors():
        yal_let.errorsManager.printErrors('✖ Identities extraction failed')
        return
    print('✔ Identities extraction successful')

    if draw_subtrees:
        if len(yal_let.idents) == 0:
            print('✔ No subtrees to draw')
        else:
            print('✔ Drawing subtrees:')
            for idx, ident in enumerate(yal_let.idents.keys()):
                this_expression: Expression = Expression(yal_let.idents[ident])
                this_expression.hardProcess()
                this_ast: AST = AST(this_expression.infixRegEx)
                this_ast.draw(ident, dir_name, ident, False)
                print(f'\t[{idx}] \"{ident}\" AST has been drawn successfully')
    else:
        print('✔ Subtrees drawing skipped, as per user request')

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

    if yal_rule.errorsManager.haveErrors():
        yal_rule.errorsManager.printErrors(
            '✖ Rule extraction failed')
        return
    elif len(yal_rule.reminders) == 0:
        print('✖ No rule found')
        print('\tError: No rule found')
        print('\tSuggestion: Check you have a rule defined in your .yal file')
        return
    print('✔ Rule extraction successful')

    print('✔ Building the final AST')

    rule_lexer = Tokenizer()
    rule_lexer.symbolsTable = yal_rule.reminders
    rule_lexer.removeSymbols([WS])

    final_expression: list = []

    for symbol in rule_lexer.symbolsTable:
        if symbol.type == ID.name:
            get_original = yal_let.idents.get(symbol.original, None)
            if get_original:
                final_expression.extend(yal_let.idents[symbol.original])
            else:
                print(f'✖ Final expression building failed:')
                print(f'\tError: \"{symbol.original}\" is not defined')
                print(f'\tSuggestion: Check the rule definition on your .yal file')
                return
        else:
            final_expression.extend(symbol.original)

    final_expression: Expression = Expression(final_expression)
    final_expression.hardProcess()

    final_ast: AST = AST(final_expression.infixRegEx)

    if final_ast.errorsManager.haveErrors():
        final_ast.errorsManager.printErrors('✖ Final AST building failed')
        print('\tSuggestion: Check the rule definition on your .yal file')
        return

    final_ast.draw('FINAL_AST', dir_name, 'FINAL AST', False)
    print('✔ Final AST building and rendering has been completed successfully')
    print('✔ All Done!')


if __name__ == "__main__":
    main()
    print('Exiting...')
