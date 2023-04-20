from app.layer.exception import AuthenticationError, WrongActionError, WrongDayError

EXCEPTIONS_HANDLING_MIDDLEWARE: tuple = (
    AuthenticationError,
    WrongActionError,
    WrongDayError,
)
