import argparse


class Error(object):
    '''
    This class represents an error.
    '''

    def __init__(self, error: str, consequence: str):
        '''
        This is the constructor of the class.
        Parameters:
        - error: A string representing the error.
        - consequence: A string representing the consequence of the error.
        '''
        self.error = error
        self.consequence = consequence


class errorsManager(object):
    '''
    This class represents the errors manager.
    '''

    def __init__(self):
        '''
        This is the constructor of the class.
        '''
        self.errors: list[Error] = []

    def haveErrors(self) -> bool:
        '''
        This function returns True if there are errors in the errors list, False otherwise.
        '''
        return len(self.errors) > 0

    def addError(self, error: str, consequence: str):
        '''
        This function adds an error to the errors list.
        Parameters:
        - error: A string representing the error.
        - consequence: A string representing the consequence of the error.
        '''
        self.errors.append(Error(error, consequence))

    def printErrors(self, scope: str):
        '''
        This function prints all the errors in the errors list.
        '''
        if self.errors:
            print(f'{scope}')
            for error in self.errors:
                print(
                    f'\tError: {error.error}, Consequence: {error.consequence}')
        else:
            print(f'No errors in {scope}')


def readYalFile(file: str) -> str:
    '''
    This function reads a YAL file and returns its content.
    Parameters:
    - file: A string representing the file name.
    Returns:
    - The content of the file.
    '''
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()


def numberToLetter(number: int) -> str:
    '''
    This function return a letter from A to Z based on the number.
    If the number is greater than 26, it calls itself recursively using the difference between the number and 26 to obtain a new combination.
    '''
    if number <= 26:
        return chr(96 + number)
    else:
        return numberToLetter((number - 1) // 26) + numberToLetter((number - 1) % 26 + 1)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
