from src._lexer import Lexer
from src.utils.tools import readYalFile
from src.utils.patterns import ID, WS, EQ, EXPR, COMMENT, RETURN


def main():
    file = input("Enter the file name: ")
    fileContent = readYalFile(file)
    print(fileContent)
    lexer = Lexer(fileContent)
    lexer.addPatterns([COMMENT, WS, ID, EQ, EXPR, RETURN])
    lexer.buildPatterns()
    lexer.tokenize()
    lexer.removeSymbols([COMMENT, WS])

    for symbol in lexer.symbolsTable:
        print(symbol)


if __name__ == "__main__":
    main()
