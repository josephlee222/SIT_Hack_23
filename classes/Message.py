from time import time

class Message:
    def __init__(self, userId, connectionId, message, nickname):
        self.id = int(time() * 1000)
        try:
            self.userId = str(userId)
            self.nickname = str(nickname)
            self.connectionId = int(connectionId)
            self.message = str(message)
        except ValueError:
            print("Value error while creating User class")