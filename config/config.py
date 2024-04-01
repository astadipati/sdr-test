import mysql.connector as mysql
from pymongo import MongoClient


class Config:

    def __init__(self, cfg):
        self.config = cfg

    def connectDB(self):
        return mysql.connect(
            user=self.config['DB_USERNAME'],
            password=self.config['DB_PASSWORD'],
            host=self.config['DB_HOST']

        )  # connect to mariaBD

    def connectMongo(self):
        # connect to mongo
        return MongoClient(self.config['URLMONGO'])
    
    def server(self):
        return {
            "ip":self.config['IP'],
            "uname":self.config['UNAME'],
            "passwd":self.config['PASSWD']
        }