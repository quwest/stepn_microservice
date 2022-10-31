import werkzeug.exceptions as ex

class IncorrectId(ex.HTTPException):
    code = 205
    description = 'incorrect project id'

class NoId(ex.HTTPException):
    code = 206
    description = 'no id'

class IncorrectArgument(ex.HTTPException):
    code = 203
    description = 'incorrect argument'

class InauthorizedAccount(Exception):
    ...
