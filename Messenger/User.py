class User:
    def __init__(self, name, connection):
        self.name = name
        self.__connection = connection
        self.visible = True

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_connection(self, connection):
        self.__connection = connection

    def get_connection(self):
        return self.__connection

    def set_visible(self, bool):
        self.visible = bool

    def is_visible(self):
        return self.visible




