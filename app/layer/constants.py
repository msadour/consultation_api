from app.layer.exception import AuthenticationError, WrongActionError, WrongTimeError

EXCEPTIONS_HANDLING_MIDDLEWARE: tuple = (
    AuthenticationError,
    WrongActionError,
    WrongTimeError,
)

SPECIALITIES: tuple = (
    ("Plastic", "Plastic"),
    ("Orthopaedic", "Orthopaedic"),
    ("Ophthalmology Surgery", "Ophthalmology Surgery"),
    ("Generalist", "Generalist"),
)
