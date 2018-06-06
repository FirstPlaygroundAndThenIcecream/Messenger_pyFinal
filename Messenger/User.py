class User:
    'Base class for all users'

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def getUsername(self):
        return self.name

    def getUserID(self):
        return self.id

    