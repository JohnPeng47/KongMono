from pymongo import MongoClient
from typing import Dict

class DBConnection:
    def __init__(self, host='18.222.249.14', port=27017, username=None, password=None):
    # def __init__(self, host='localhost', port=8081, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.db = None
        self.connected = False

        DATABASE = "kongbot"
        self.connect(DATABASE)

    def connect(self, database):
        try:
            self.client = MongoClient(self.host, self.port)
            self.db = self.client[database]

            if self.username and self.password:
                self.db.authenticate(self.username, self.password)

            self.connected = True
            print(f"Connected to database '{database}'")
        except Exception as e:
            print(f"Failed to connect to database: {e}")

    def disconnect(self):
        try:
            self.client.close()
            print("Disconnected from database")
        except Exception as e:
            print(f"Failed to disconnect from database: {e}")

    def get_collection(self, collection):
        if self.connected:
            return self.db[collection]
        else:
            print("Not connected to any database")
    
    ### For books
    def insert_book(self, book: Dict):
        self.get_collection("kong_book").insert_one(book)