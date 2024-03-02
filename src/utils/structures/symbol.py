
class Symbol(object):
    '''
    This class represents a symbol.
    '''

    def __init__(self, type: str, content: str, original: str):
        '''
        This is the constructor of the class.
        Parameters:
        - name: The name of the symbol.
        - lexeme: The lexeme of the symbol.
        '''
        self.type: str = type
        self.content: str = content
        self.original: str = original

    def __str__(self) -> str:
        '''
        This function returns the string representation of the symbol.
        '''
        return f'{self.type} -> {self.content} -> {self.original}'
