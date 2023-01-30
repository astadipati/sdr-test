from config.config import Config
import pandas as pd


class Master_sdr(Config):
    def __init__(self, cfg):
        self.cfx = Config(cfg)

    def get_sites(self):
        try:
            conn = self.cfx.connectDB()

            cursor = conn.cursor(dictionary=True)
            query = "SELECT * from iperf.sites"
            cursor.execute(query)

            data = cursor.fetchall()

            conn.close()
            return data
            pass

        except Exception as e:
            raise e

    def get_sites_status_on(self):
        try:
            conn = self.cfx.connectDB()

            cursor = conn.cursor(dictionary=True)
            query = "SELECT * from iperf.sites WHERE status = 1"
            cursor.execute(query)

            data = cursor.fetchall()

            conn.close()
            return data
            pass

        except Exception as e:
            raise e

    def get_sites_status_off(self):
        try:
            conn = self.cfx.connectDB()

            cursor = conn.cursor(dictionary=True)
            query = "SELECT * from iperf.sites WHERE status = 0"
            cursor.execute(query)

            data = cursor.fetchall()

            conn.close()
            return data
            pass

        except Exception as e:
            raise e

    def update_single_sites(self, id, post):
        try:
            conn = self.cfx.connectDB()

            cursor = conn.cursor(dictionary=True)
            query = "UPDATE iperf.sites SET terminal = 'mary.patterson@classicmodelcars.com WHERE employeeNumber = 1056"
            cursor.execute(query)

            data = cursor.fetchall()

            conn.close()
            return data
            pass

        except Exception as e:
            raise e
