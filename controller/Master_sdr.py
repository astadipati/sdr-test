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

            return None
