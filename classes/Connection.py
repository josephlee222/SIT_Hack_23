from time import time

class Connection:
    def __init__(self, userId, councilId, nickname):
        self.id = int(time() * 1000)
        try:
            self.userId = str(userId)
            self.councilId = str(councilId)
            self.status = True
            self.feedback = False
            self.nickname = nickname
        except ValueError:
            print("Value error while creating Connection class")