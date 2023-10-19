from config.config import Config
import pandas as pd
from datetime import datetime, timedelta
import time
import subprocess
import requests
import json



class Master_sdr(Config):
    
    def __init__(self, cfg):
        self.cfx = Config(cfg)
        
    def add_mini_pc(self, post):
        try:
            date = datetime.now()
            date = date.replace(microsecond=0)
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""INSERT INTO iperf.sites (name,ip,port_server,user,pass,ip_server,status, bitrate, duration, subscriber_number,beam, created_at) 
            VALUES('{post.name}','{post.ip}','{post.port_server}','{post.user}','{post.passwd}','{post.ip_server}',{post.status},{post.bitrate},{post.duration},'{post.subscriber_number}','{post.beam}', '{date}') """
            cursor.execute(query)
            conn.commit()
            conn.close()
            return 
        except Exception as e:
            raise e
        
    def del_mini_pc(self, id):
        
        try:
            date = datetime.now()
            date = date.replace(microsecond=0)
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"DELETE FROM iperf.sites WHERE id='{id}'"
            cursor.execute(query)
            conn.commit()
            conn.close()
            return 
        except Exception as e:
            raise e
        
    def get_status_port(self):
        try:
            uri = self.cfx.config['URL_SNT']
            print(url)
            url = uri+"/flux/api/server/statusport"

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
            uri = self.cfx.config['URL_SNT']
            url = uri+"/flux/api/server/statusport"

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

                subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -p {port} -t {time_processing} -R > /dev/null 2>/dev/null &",
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

        subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -p {port} -t {time_processing} > /dev/null 2>/dev/null &",
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
            
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = """SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.ip_server, sites.port_server, sites.ip_server,
                        sites.status ,sites.updated_at from iperf.sites"""
            cursor.execute(query)
            data = cursor.fetchall()
            # conn.close()
            df = pd.DataFrame(data)
            # print(df)
            # status = df['status']
            st = []
            for i in range(len(df['status'])):
                t = df['status'][i]
                if t == 1:
                    st.append("Active")
                else:
                    st.append("Not Active")
            # return st
            df['status'] = st
            
            # # status port
            url = uri+"/flux/api/server/statusport"

            payload = {}
            headers = {}

            r = requests.request("GET", url, headers=headers, data=payload)
            r = r.json()
            # print(r.text)
            temp_statusport = []
            for j in r:
                temp_statusport.append(j['status_port'])
            df['status_port']=temp_statusport
            # print(df)
            val = df.loc[:, ['id','subscriber_number','name','ip','ip_server', 'port_server','status_port','status','updated_at']]
            # df = df.loc[:,'id']
            to_dict = val.to_dict("records")
            # print(df)

            return to_dict

        except Exception as e:
            raise e
        
    def get_sites_active(self):
        try:
            
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = """SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.ip_server, sites.port_server, sites.ip_server,
                        sites.status ,sites.updated_at from iperf.sites where sites.status=1"""
            cursor.execute(query)
            data = cursor.fetchall()
            # conn.close()
            df = pd.DataFrame(data)
            # print(df)
            # status = df['status']
            st = []
            for i in range(len(df['status'])):
                t = df['status'][i]
                if t == 1:
                    st.append("Active")
                else:
                    st.append("Not Active")
            # return st
            df['status'] = st
            
            # # status port
            url = uri+"/flux/api/server/statusport"

            payload = {}
            headers = {}

            r = requests.request("GET", url, headers=headers, data=payload)
            r = r.json()
            # print(r.text)
            temp_statusport = []
            for j in r:
                temp_statusport.append(j['status_port'])
            df['status_port']=temp_statusport
            # print(df)
            val = df.loc[:, ['id','subscriber_number','name','ip','ip_server', 'port_server','status_port','status','updated_at']]
            # df = df.loc[:,'id']
            to_dict = val.to_dict("records")
            # print(df)

            return to_dict

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
        
    def get_tr_on(self):
        try:
            now = datetime.now()
            now = now.replace(microsecond=0, second=0)
            now = now.strftime("%H:%M:%S")
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = """SELECT a.id, a.subscriber_number, a.name, a.ip, a.port_server, a.ip_server, a.status, a.bitrate, a.duration, b.timee, a.updated_at 
                    from iperf.sites a
                    left join iperf.scheduler b on a.id = b.sites_id 
                    """
            cursor.execute(query)
            data = cursor.fetchall()
            # conn.close()
            df = pd.DataFrame(data)
            print(df)
            # return 9
            url = uri+"/flux/api/zabbix/status"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            res = response.json()
            # print(res)
            
            temp = []
            for i in res:
                # print(i['lastvalue'])
                temp.append(i['lastvalue'])
            df['status']=temp
            tf = df.loc[df['status'].isin(['1'])]
            print(tf)
            # to_dict = tf.to_dict("records")
            # print(df)

            return "to_dict"

        except Exception as e:
            raise e
        
    # update status tr
    def put_tr_status(self):
        try:
            now = datetime.now()
            now = now.replace(microsecond=0, second=0)
            now = now.strftime("%H:%M:%S")
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            
            # print(df)
            # return 9
            url = uri+"/flux/api/zabbix/status"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            res = response.json()
            # print(res)
            df = pd.DataFrame(res)
            # print(df['lastvalue'])
            temp = []
            for i in range(len(df['ip'])):
                ip = df['ip'][i]
                # print(ip)
                status = int(df['lastvalue'][i])
                print(status)
                # if status == 1:
                #     temp.append(status)
                # else:
                #     pass
                # return 8
                query = f"""UPDATE iperf.sites 
                            SET status = {status}
                            WHERE ip='{ip}'"""
                
                cursor.execute(query)
                conn.commit()
                # conn.close()
                # temp.append(ip)
            
            return temp

        except Exception as e:
            raise e

    # used for detil
    def get_single_sites(self, id):
        try:
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT sites.id, sites.subscriber_number, sites.name, sites.user,sites.ip, sites.ip_server, sites.port_server, sites.ip_server,sites.status,
                        sites.duration ,sites.updated_at from iperf.sites WHERE id = {id}"""
            cursor.execute(query)
            data = cursor.fetchall()
            # print(data)
            # df = pd.DataFrame(data)
            id_mini = data[0]['id']
            sbc = data[0]['subscriber_number']
            name = data[0]['name']
            user = data[0]['user']
            ip = data[0]['ip']
            port_server = data[0]['port_server']
            ip_server = data[0]['ip_server']
            if data[0]['status']==1:
                status="Active"
            else:
                status="Not Active"
            duration = data[0]['duration']
            # df = pd.DataFrame(data)
            # print(df)
            conn.close()
            
            url = uri+"/flux/api/server/statusport"

            payload = {}
            headers = {}

            r = requests.request("GET", url, headers=headers, data=payload)
            r = r.json()
            # print(r)
            # print(ip)
            temp_statusport = []
            for j in r:
                if j['ip']==ip:
                    temp_statusport.append(j['status_port'])
                else:
                    pass
            # print(temp_statusport[0])
           
            return {
                "id": id_mini,
                "subscriber_number":sbc,
                "name":name,
                "user":user,
                "ip":ip,
                "ip_server":ip_server,
                "port_server":port_server,
                "status_port":temp_statusport[0],
                "status":status,
                "duration":duration
            }
            
        except Exception as e:
            raise e
        
    def get_single_chart(self, id):
        # now = datetime.now()
        # now = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT sites.id, sites.ip from iperf.sites WHERE id = {id}"""
            cursor.execute(query)
            data = cursor.fetchall()
            ip = data[0]['ip']
            conn.close()
            
            date = datetime.now()

            delta = date - timedelta(hours=1)

            selisih = date - delta
            # print("selisih: ", selisih)

            # print("delta: ",delta)
            st_date = str(delta.replace(microsecond=0))

            dt_timestamp = int(time.mktime(datetime.strptime(st_date, "%Y-%m-%d %H:%M:%S").timetuple()))
            # print(dt_timestamp)

            url = uri+"/zabbix/api_jsonrpc.php"

            payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "edy",
                "password": "Kul0nuwun"
            },
            "id": "1"
            })
            headers = {
            'Content-Type': 'application/json'
            }

            # get itemid
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            token = data['result']
            # get download id
            payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                    "output": ["itemid","key_","lastvalue","lastclock"],
                    "host" : ip,
                    "filter": {
                        "key_": ["net.if.in[\"eth0\"]","net.if.out[\"eth0\"]"]
                    },
                    "sortfield": "name"
                },
            "auth": token,
            "id": 1
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            result = data['result']
            # print(result)
            df = pd.DataFrame(result)
            # get itemid for download and upload
            download_id = df['itemid'][0]
            upload_id = df['itemid'][1]

            # get history download
            payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": download_id,
                "sortfield": "clock",
                "sortorder": "ASC",
                "time_from": dt_timestamp
            },
            "auth": token,
            "id": 1
            })
            headers = {
            'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            res_download = data['result']
            temp_download = []
            for j in res_download:
                val_do = (int(j['value']))/1000
            # print(to)
                temp_download.append(val_do)
            # print(temp_download)
            # exit()
            df2 = pd.DataFrame(res_download)
            # print(res_download)
            temp_time = []
            for k in res_download:
                cl = int(k['clock'])
                to_obj = datetime.fromtimestamp(cl)
            #   # print(to_obj)
                temp_time.append(to_obj)
            df2['val_download']=temp_download
            df2['time']=temp_time
            # temp_download
            # temp_time
            # get history upload
            payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": upload_id,
                "sortfield": "clock",
                "sortorder": "ASC",
                "time_from": dt_timestamp
            },
            "auth": token,
            "id": 1
            })
            headers = {
            'Content-Type': 'application/json'
            }

            r2 = requests.request("POST", url, headers=headers, data=payload)
            data_upload = r2.json()
            res_upload = data_upload['result']
            temp_upload = []
            for u in res_upload:
                val_up = (int(u['value']))/1000
            # print(to)
                temp_upload.append(val_up)
            df2['val_upload']=temp_upload
            df2 = df2.loc[:,['val_download','val_upload','time']]
            return df2.to_dict("records")

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
            # print(query)
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
            return

        except Exception as e:
            raise e
        
    def get_scheduler_all(self):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT b.id, a.timee, a.tipe, a.duration FROM iperf.scheduler a LEFT JOIN iperf.sites b 
                        ON a.sites_id = b.id """
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            raise e

    def get_scheduler(self, id):
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT b.id, a.timee, a.tipe, a.duration FROM iperf.scheduler a LEFT JOIN iperf.sites b 
                        ON a.sites_id = b.id WHERE b.id = {id}"""
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e
                
    # ini akan kebaca buat scheduler
    def get_scheduler_kratos(self):
        now = datetime.now()
        now = now.strftime("%Y-%m-%d")
        
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT b.id, b.name, b.duration, a.timee, a.tipe, a.comments 
                        FROM iperf.scheduler a 
                        LEFT JOIN iperf.sites b ON a.sites_id = b.id"""
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            start = []
            end = []
            val_fwd_rtn = []
            for i in df['timee']:
                # print(str(i)[7:-3])
                start.append(str(i)[7:-3])
            do_up = df['tipe']
            val_fwd_rtn = []
            for n in do_up:
                if n=="d":
                    val_fwd_rtn.append("FWD")
                else:
                    val_fwd_rtn.append("RTN")

            df['date']=now                
            df['start_time']=start
            df['terminal_id']=df['name']
            df['duration']=df['duration']
            df['fwd_rtn_selection']=val_fwd_rtn
            val = df.loc[:, ['id','date','start_time','terminal_id','duration','fwd_rtn_selection']]
            conn.close()
            return val.to_dict('records')

        except Exception as e:
            raise e
        
    def post_scheduler(self, post):
        now = datetime.now()
        now = now.replace(microsecond=0)
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""INSERT INTO iperf.scheduler (sites_id, tipe, timee, duration, date_created) 
                        VALUES({post.sites_id}, '{post.tipe}', '{post.timee}','{post.duration}','{now}')"""
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
            query = f"""UPDATE iperf.scheduler SET 
                        sites_id={post.sites_id}, tipe='{post.tipe}', timee='{post.timee}', duration='{post.duration}', 
                        updated_at='{now}' WHERE id={id}"""
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
