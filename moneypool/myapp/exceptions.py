class Error(Exception):
    error = ""
    message = ""
    pass

class alreadyAttending(Error):
    def __init__(self, message):
        self.error = "Error Joining Trip"
        self.message = message
    pass

class alreadyInvited(Error):
    def __init__(self, message):
        self.error = "Error Inviting User"
        self.message = message
    pass