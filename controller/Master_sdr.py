from config.config import Config
import pandas as pd
from datetime import datetime
import time
import subprocess
import requests



class Master_sdr(Config):
    def __init__(self, cfg):
        self.cfx = Config(cfg)
    def add_mini_pc(self, post):
        try:
            date = datetime.now()
            date = date.replace(microsecond=0)
            conn = self.cfx.connectDB()
            # pas = post.pass
            cursor = conn.cursor(dictionary=True)
            query = f"""INSERT INTO iperf.sites (name,ip,port_server,user,pass,ip_server,status, bitrate, duration, subscriber_number,beam, created_at) 
            VALUES('{post.name}','{post.ip}','{post.port_server}','{post.user}','{post.passwd}','{post.ip_server}',{post.status},{post.bitrate},{post.duration},'{post.subscriber_number}','{post.beam}', '{date}') """
            cursor.execute(query)
            conn.commit()
            conn.close()
            return 
        except Exception as e:
            raise e
        
    def get_status_port(self):
        try:

            url = "http://192.168.1.220/flux/api/server/statusport"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()
            return data
        except Exception as e:
            raise e

    def download(self, uname, ip_tr, ip_server, port, time_processing):
        start = time.time()
        print(ip_tr)
        try:
            url = "http://192.168.1.220/flux/api/server/statusport"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()
            df = pd.DataFrame(data)
            # print(df)
            
            df = df.loc[df['ip']==ip_tr]
            val = df['status_port'].values[0]
       
            if val=='listen':
                print("jalankan")

                subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -p {port} -t {time_processing} -b 10m -R > /dev/null 2>/dev/null &",
                                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                info = {
                    "status": "sukses",
                    "data": {
                        "Name":uname,
                        "Port":port,
                        "Time":time_processing,
                        "Executed": "%s seconds" % (time.time() - start)
                    }
                }
            else:
                info = {
                    "status": f"Port {port} terpakai, tidak dapat melakukan test SDR",
                    "data": {
                        "Name":uname,
                        "Port":port,
                        "Time":time_processing,
                        "Executed": "%s seconds" % (time.time() - start)
                    }
                }
            
            return info
        except Exception as e:
            raise e

    def upload(self, uname, ip_tr, ip_server, port, time_processing):

        start = time.time()

        subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -p {port} -t {time_processing} -b  10m > /dev/null 2>/dev/null &",
                                     shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        info = {
            "status": "200",
            "data": {
                "Name":uname,
                "Port":port,
                "Time":time_processing,
                "Executed": "%s seconds" % (time.time() - start)
            }
        }
        return info

    def get_sites(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites"
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
            query = "SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE status = 1"
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
            query = "SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE status = 0"
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
            query = f"SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.port_server, sites.ip_server,sites.status ,sites.updated_at from iperf.sites WHERE id = {id}"
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

    def update_status_mini(self, id, post):
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
            query = f"UPDATE iperf.sites SET name='{post.name}', subscriber_number='{post.subscriber_number}',ip='{post.ip}',port_server='{post.port_server}',user='{post.user}',ip_server = '{post.ip_server}', duration='{post.duration}', updated_at = '{now}', subscriber_number = '{post.subscriber_number}' WHERE id = {id}"
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

    def get_scheduler_paginate(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT b.id, a.timee, a.tipe, a.comments FROM iperf.scheduler a LEFT JOIN iperf.sites b ON a.sites_id = b.id"
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

    def get_val_max_download_today(self, device_id):
        device = device_id.upper()
        try:
            date = datetime.now()
            ed = date.replace(hour=0, minute=0, second=0, microsecond=0)
            # print(ed)
            # st = ed - timedelta(hours=24)
            conn = self.cfx.connectMongo()
            db = conn.nms_n5
            col = db.data_sdr_module.find(
                {"deviceID": device, "date_created": {'$gte': ed}, "download": {"$exists": "true"}}).sort("_id", -1)
            data_dict = []
            for i in col:
                del i["_id"]
                data_dict.append(i)
            df = pd.DataFrame(data_dict)
            limit = int(len(df))-1
            # print(df)
            # exit()
            val_temp = []
            for i in range(limit):
                # 1048576
                total = (
                    # kbps
                    # ((df["download"][i]-df"download"][i+1])*8)/307200)
                    # mbps
                    ((df["download"][i]-df["download"][i+1])*8)/314572800)
                val_temp.append(total)
            df['deviceID'] = device
            df['max_val'] = pd.DataFrame(val_temp)
            df['date_created'] = datetime.now().replace(second=0, microsecond=0)
            df = pd.DataFrame.max(df)
            data = df.to_dict()
            return data

        except Exception as e:
            raise e

    def get_val_max_upload_today(self, device_id):
        device = device_id.upper()
        try:
            date = datetime.now()
            ed = date.replace(hour=0, minute=0, second=0, microsecond=0)
            # print(ed)
            # st = ed - timedelta(hours=24)
            conn = self.cfx.connectMongo()
            db = conn.nms_n5
            col = db.data_sdr_module.find(
                {"deviceID": device, "date_created": {'$gte': ed}, "upload": {"$exists": "true"}}).sort("_id", -1)
            data_dict = []
            for i in col:
                del i["_id"]
                data_dict.append(i)
            df = pd.DataFrame(data_dict)
            limit = int(len(df))-1
            # print(df)
            # exit()
            val_temp = []
            for i in range(limit):
                # 1048576
                total = (
                    ((df["upload"][i]-df["upload"][i+1])*8)/314572800)
                val_temp.append(total)
            df['deviceID'] = device
            df['max_val'] = pd.DataFrame(val_temp)
            df['date_created'] = datetime.now().replace(second=0, microsecond=0)
            df = pd.DataFrame.max(df)
            data = df.to_dict()
            return data

        except Exception as e:
            raise e
