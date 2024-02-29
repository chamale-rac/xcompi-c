from src.utils.constants import MINOR_LETTERS, MAJOR_LETTERS


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
    f'[{MAJOR_LETTERS}{MINOR_LETTERS}]+'
)
