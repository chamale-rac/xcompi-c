from src._expression import Expression
from src._ast import AbstractSyntaxTree as AST
from src._dir_dfa import DirectDeterministicFiniteAutomaton as DirDFA
from src._min_dfa import MinimizedDeterministicFiniteAutomaton as MinDFA


class Pattern(object):
    '''
    This class represents the pattern module.
    '''

    def __init__(self,
                 name: str,
                 pattern: str) -> None:

        self.name: str = name
        self.pattern: str = pattern

    def build(self, idx: int) -> None:
        '''
        This function builds the DFA for the pattern.
        '''
        # print(self.name)
        self.expr = Expression(self.pattern)
        self.expr.infixRegEx = self.expr.hardCodify(
            self.expr.infixRegEx
        )
        self.expr.infixRegEx = self.expr.transformGroupsOfCharacters(
            self.expr.infixRegEx
        )

        # print('transformGroupsOfCharacters')
        # print(self.expr.infixRegEx)
        self.expr.infixRegEx = self.expr.addExplicitConcatenation(
            self.expr.infixRegEx
        )

        # print('addExplicitConcatenation')
        # print(self.expr.infixRegEx)
        self.expr.infixRegEx = self.expr.shuntingYard(
            self.expr.infixRegEx
        )

        # print('shuntingYard')
        # print(self.expr.infixRegEx)
        self.ast = AST(self.expr.infixRegEx)
        self.dir_dfa = DirDFA(self.ast.root.deepCopy())
        self.min_dir_dfa = MinDFA(self.dir_dfa, self.ast.alphabet)
        # self.min_dir_dfa.draw(
        #     'Min Dir DFA', idx, self.name
        # )
        # self.dir_dfa.draw(
        #     'Dir DFA', idx, self.name
        # )


ID = Pattern(
    'ID',
    f"['a'-'z']+"
)

WS = Pattern(
    'WS',
    f"( |['\t''\n'])+"
)

EQ = Pattern(
    'EQ',
    f"="
)

EXPR = Pattern(
    'EXPR',
    f"(['A'-'Z''a'-'z''0'-'9']|\\\'|\-|\(\)\[\]\+\*\?|.\|)+"
)

COMMENT = Pattern(
    'COMMENT',
    f"\(\*(['A'-'Z''a'-'z''0'-'9']|\t| |,|\.|\-|(á|é|í|ó|ú))*\*\)"
)
