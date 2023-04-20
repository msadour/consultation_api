class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 400
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 404
        super().__init__(self.message)


class WrongActionError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 400
        super().__init__(self.message)


class WrongDayError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 400
        super().__init__(self.message)
