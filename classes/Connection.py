from time import time

class Connection:
    def __init__(self, userId, councilId):
        self.id = int(time() * 1000)
        try:
            self.userId = str(userId)
            self.councilId = int(councilId)
        except ValueError:
            print("Value error while creating User class")