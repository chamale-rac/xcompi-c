
class Pattern(object):
    '''
    This class represents the pattern module.
    '''

    def __init__(self,
                 name: str,
                 pattern: str) -> None:

        self.name: str = name
        self.pattern: str = pattern


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
    f"(['a'-'z'])"
)

COMMENT = Pattern(
    'COMMENT',
    f"\(\*(['A'-'Z''a'-'z''0'-'9']|\t| |,|\.|\-|(á|é|í|ó|ú))*\*\)"
)
