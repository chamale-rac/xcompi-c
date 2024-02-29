from src._expression import Expression
from src.utils.tools import readYalFile


class App:
    def __init__(self):
        test_expressions = [
            "['0'-'9']",
            "[' ''\t''\n']",
            "['A'-'Z''a'-'z']",
            '["\s\t\n"]+'
        ]
        for test_expression in test_expressions:
            self.expression = Expression(test_expression)
            self.expression.infixRegEx = self.expression.hardCodify(
                self.expression.infixRegEx
            )
            self.expression.infixRegEx = self.expression.transformGroupsOfCharacters(
                self.expression.infixRegEx
            )
            print(self.expression.infixRegEx)


app = App()
