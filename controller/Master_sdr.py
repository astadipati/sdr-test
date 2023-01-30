from config.config import Config
import pandas as pd
from datetime import datetime


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

    def get_single_sites(self, id):
        try:
            conn = self.cfx.connectDB()

            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * from iperf.sites WHERE id = {id}"
            cursor.execute(query)

            data = cursor.fetchall()

            conn.close()
            return data

        except Exception as e:
            raise e

    def update_single_sites(self, id, post):
        print(f"id: {id} post: {post}")
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            # query = f"UPDATE iperf.sites SET {post}, updated_at = '{now}' WHERE id = {id}"
            query = f"UPDATE iperf.sites SET status='{post}', updated_at = '{now}' WHERE id = {id}"
            print(query)
            cursor.execute(query)
            conn.commit()
            conn.close()
            return "ok"

        except Exception as e:
            raise e
