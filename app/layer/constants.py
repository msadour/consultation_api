from app.layer.exception import AuthenticationError


EXCEPTIONS_HANDLING_MIDDLEWARE: tuple = (AuthenticationError,)
