"""
Exception handling for Freebase
"""

class FreebaseException(Exception):

    def __init__(self, **kwargs):
        """
        Pass in the Python dictionary of the response containing the error
        directly and this class will handle the error details.
        """

        if 'error' not in kwargs:
            error = {
                'code': 520,
                'domain': 'pythonFreebase',
                'message': 'Unknown Python Freebase exception',
                'reason': 'UnknownException',
                'extendedHelp': None
            }
        else:
            error = kwargs['error']['errors'][0]
            error['code'] = kwargs['error']['code']

        for k,v in error.items():
            setattr(self, k, v)

        super(FreebaseException, self).__init__(self.message)

    def __str__(self):
        return "%s Error (%i) - %s: %s" % (self.domain, self.code, self.reason, self.message)
