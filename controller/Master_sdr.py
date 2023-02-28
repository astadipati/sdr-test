from config.config import Config
import pandas as pd
from datetime import datetime
import time
import subprocess


class Master_sdr(Config):
    def __init__(self, cfg):
        self.cfx = Config(cfg)

    def download(self, uname, ip_tr, ip_server, port, time_processing):

        start = time.time()

        print(f"do download test {uname}")

        myprocess = subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -p {port} -t {time_processing} -b 10m -R > /dev/null 2>/dev/null &",
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        finish = time.time()
        print(f"SDR {uname} finished {round(start-finish),2} second(s)")
        return myprocess

    def upload(self, uname, ip_tr, ip_server, port, time_processing):

        start = time.time()

        print(f"do upload test {uname}")
        myprocess = subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -p {port} -t {time_processing} -b  10m > /dev/null 2>/dev/null &",
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        finish = time.time()
        print(f"SDR {uname} finished {round(start-finish),2} second(s)")
        return myprocess

    def get_sites(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT sites.id, sites.subscriber_id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites"
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
            query = "SELECT sites.id, sites.subscriber_id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE status = 1"
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
            query = "SELECT sites.id, sites.subscriber_id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE status = 0"
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
            query = f"SELECT sites.id, sites.subscriber_id, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE id = {id}"
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

    def update_mini_pc(self, id, post):
        print(post)
        now = datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            # query = f"UPDATE iperf.sites SET {post}, updated_at = '{now}' WHERE id = {id}"
            query = f"UPDATE iperf.sites SET name='{post.name}', subscriber_id='{post.subscriber_id}',ip='{post.ip}',port_server='{post.port_server}',user='{post.user}',ip_server = '{post.ip_server}', duration='{post.duration}', updated_at = '{now}' WHERE id = {id}"
            # print(query)
            cursor.execute(query)
            conn.commit()
            conn.close()
            return "ok"

        except Exception as e:
            raise e

    def get_scheduler(self, id):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT b.id, a.timee, a.tipe, a.comments FROM iperf.scheduler a LEFT JOIN iperf.sites b ON a.sites_id = b.id WHERE b.id = {id}"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e

    def post_scheduler(self, post):
        now = datetime.now()
        now = now.replace(microsecond=0)
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"INSERT INTO iperf.scheduler (sites_id, tipe, timee, comments, date_created) VALUES({post.sites_id}, '{post.tipe}', '{post.timee}','{post.comments}','{now}')"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return

        except Exception as e:
            raise e

    def update_scheduler(self, id, post):
        now = datetime.now()
        now = now.replace(microsecond=0)
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"UPDATE iperf.scheduler SET sites_id={post.sites_id}, tipe='{post.tipe}', timee='{post.timee}', comments='{post.comments}', updated_at='{now}' WHERE id={id}"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return

        except Exception as e:
            raise e

    def delete_scheduler(self, id):

        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"DELETE FROM iperf.scheduler WHERE id={id}"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return

        except Exception as e:
            raise e
