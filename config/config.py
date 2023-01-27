import mysql.connector as mysql


class Config:

    def __init__(self, cfg):
        self.config = cfg

    def connectDB(self):
        return mysql.connect(
            user=self.config['DB_USERNAME'],
            password=self.config['DB_PASSWORD'],
            host=self.config['DB_HOST']

        )  # connect to mariaBD
