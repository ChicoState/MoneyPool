from django.db import IntegrityError


class Error(Exception):
    error = ""
    message = ""
    pass

class AlreadyExistsError(Error):
    def __init__(self, message):
        self.error = "Error Adding Friend"
        self.message = message
    pass


class AlreadyFriendsError(Error):
    def __init__(self, message):
        self.error = "Error Adding Friend"
        self.message = message
    pass
