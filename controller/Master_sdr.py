from config.config import Config
import pandas as pd
from datetime import datetime
import time
import subprocess


class Master_sdr(Config):
    def __init__(self, cfg):
        self.cfx = Config(cfg)

    def runandget(self, uname, ip_tr, ip_server, port, time_processing):

        start = time.time()

        print(f"do download test {uname}")

        myprocess = subprocess.Popen(f"ssh {uname}@{ip_tr} iperf3 -c {ip_server} -p {port} -t {time_processing} -R",
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        time.sleep(10)
        print(f"do upload test {uname}")
        myprocess = subprocess.Popen(f"ssh {uname}@{ip_tr} iperf3 -c {ip_server} -p {port} -t {time_processing}",
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        finish = time.time()
        print(f"SDR {uname} finished {round(start-finish),2} second(s)")
        return myprocess

    def get_sites(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT sites.id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e

    def get_sites_status_on(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT sites.id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE status = 1"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e

    def get_sites_status_off(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT sites.id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE status = 0"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e

    def get_single_sites(self, id):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT sites.id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE id = {id}"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e

    def update_single_sites(self, id, post):
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
