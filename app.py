from src._lexer import Lexer
from src.utils.tools import readYalFile
from src.utils.patterns import ID, WS, EQ, EXPR, COMMENT


def main():
    file = input("Enter the file name: ")
    fileContent = readYalFile(file)
    print(fileContent)
    lexer = Lexer(fileContent)
    lexer.addPattern(COMMENT)
    lexer.addPattern(WS)
    lexer.addPattern(ID)
    lexer.addPattern(EQ)
    lexer.addPattern(EXPR)
    lexer.buildPatterns()


if __name__ == "__main__":
    main()
