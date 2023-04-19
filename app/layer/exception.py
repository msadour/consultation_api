class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message
        self.code = 400
        super().__init__(self.message)
