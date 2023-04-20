from app.layer.exception import AuthenticationError, WrongActionError, WrongTimeError

EXCEPTIONS_HANDLING_MIDDLEWARE: tuple = (
    AuthenticationError,
    WrongActionError,
    WrongTimeError,
)
