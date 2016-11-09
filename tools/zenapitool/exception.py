class ZenAPIBaseException(Exception):
    """ Base exception for all modules """

    # Error message prefix.
    message = '{value}'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if self.message:
            return '{error}: {details}'.format(error=self.message, details=self.value)
        else:
            return self.value
