from src._expression import Expression
from src._ast import AbstractSyntaxTree as AST
from src._dir_dfa import DirectDeterministicFiniteAutomaton as DirDFA
from src._min_dfa import MinimizedDeterministicFiniteAutomaton as MinDFA
from src.utils.constants import LPAREN, RPAREN, OR, KLEENE_STAR, ONE_OR_MORE


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
        # TODO: errors manager
        self.expr = Expression(self.pattern)
        self.expr.infixRegEx = self.expr.hardCodify(
            self.expr.infixRegEx
        )
        self.expr.infixRegEx = self.expr.transformGroupsOfCharacters(
            self.expr.infixRegEx
        )

        self.expr.infixRegEx = self.expr.addExplicitConcatenation(
            self.expr.infixRegEx
        )

        self.expr.infixRegEx = self.expr.shuntingYard(
            self.expr.infixRegEx
        )

        self.ast = AST(self.expr.infixRegEx)

        self.dir_dfa = DirDFA(self.ast.root.deepCopy())

        self.min_dir_dfa = MinDFA(self.dir_dfa, self.ast.alphabet)

    def draw(self, idx: int) -> None:
        self.ast.draw(f'{self.name}_AST', idx, f'{self.name} AST')
        self.dir_dfa.draw(f'{self.name}_DIR_DFA', idx, f'{self.name} DIR DFA')

        self.min_dir_dfa.draw(f'{self.name}_MIN_DIR_DFA',
                              idx, f'{self.name} MIN DIR DFA')

    def __str__(self) -> str:
        '''
        This function returns the string representation of the pattern.
        '''
        return f'{self.name} -> {self.pattern}'
# LEXER PASS PATTERNS


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

RETURN = Pattern(
    'RETURN',
    "\{(['A'-'Z''a'-'z']| )*\}"
)

EXPR = Pattern(
    'EXPR',
    f"(['A'-'Z''a'-'z''0'-'9'' ']|\\\'|\\\"|\-|\||\(|\)|\[|\]|\+|\*|\?|.|\\\\|/|\_|:|=|;|<)+"
)

COMMENT = Pattern(
    'COMMENT',
    f"\(\*(['A'-'Z''a'-'z''0'-'9']|\t| |,|\.|\-|(á|é|í|ó|ú))*\*\)"
)

# YAL SEQ LET PASS PATTERNS
LET = Pattern(
    ID.name,
    f"let"
)

OPERATOR = Pattern(
    'OPERATOR',
    f"(\(|\)|\+|\*|\||.|\?|\_)"
)

GROUP = Pattern(
    'GROUP',
    f"\[(['A'-'Z''a'-'z''0'-'9'' ']|\\\'|\\\"|\\\\|\-|\+)+\]"
)

CHAR = Pattern(
    'CHAR',
    f"\\'['A'-'Z''a'-'z''0'-'9'' ']\\'"
)

# YAL SEQ RULE PASS PATTERNS
RULE = Pattern(
    ID.name,
    f"rule"
)

OR = Pattern(
    EXPR.name,
    f"\|"
)
