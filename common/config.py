import os


class Config:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.dbHost = os.getenv('dbHost', '127.0.0.1')
        self.dbPort = os.getenv('dbPort', '3306')
        self.dbUserName = os.getenv('dbUserName', 'root')
        self.dbUserPassword = os.getenv('dbUserPassword', '5190')
        self.dbDatabase = os.getenv('dbDatabase', 'testdb')
