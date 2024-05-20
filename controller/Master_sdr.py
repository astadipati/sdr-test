from config.config import Config
import pandas as pd
from datetime import datetime, timedelta
import time
import subprocess
import requests
import json
import paramiko
import re
from fastapi import HTTPException

from dotenv import dotenv_values

# config = dotenv_values()

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
            url = uri+"/api/server/statusport"

            payload={}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()
            return data
        except Exception as e:
            raise e
    # FWD
    def download(self, terminal_id, uname, ip_tr, ip_server, port, time_processing):
        start = time.time()
        print(type(terminal_id))
        try:
            # date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.now()
            date = (date - timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')
            # date = date.replace(microsecond=0)
            # print(type(date))
            # print(type(time_processing))
            rtn = "RTN"
            # conn = self.cfx.connectDB()
            # cursor = conn.cursor(dictionary=True)
            # query = f"""INSERT INTO iperf.log_kratos (terminal_id,start_datetime,duration, fwd_rtn_selection) 
            #             VALUES('{terminal_id}','{date}','{time_processing}','{rtn}') """
            # cursor.execute(query)
            # conn.commit()
            try:

                subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -u -b 6M -p {port} -t {time_processing} > /dev/null 2>/dev/null &",
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                return { "status": "sukses",
                        "data": {
                            "Name":uname,
                            "Port":port,
                            "Time":time_processing,
                            "Executed": "%s seconds" % (time.time() - start)
                        }}
            except Exception as e:
                 raise HTTPException(status_code=400, detail="Bad Request")
            # return 9
            info = {
                "status": "sukses",
                "data": {
                    "Name":uname,
                    "Port":port,
                    "Time":time_processing,
                    "Executed": "%s seconds" % (time.time() - start)
                }
            }
                # conn = self.cfx.connectDB()
                # cursor = conn.cursor(dictionary=True)
                # query = f"""INSERT INTO iperf.log_kratos (terminal_id,start_datetime,duration, fwd_rtn_selection) 
                #         VALUES('{terminal_id}','{date}','{time_processing}','RTN' """
                # cursor.execute(query)
                # conn.commit()
                # conn.close()
            #     return info
            # else:
            #     info = {
            #         "status": f"Port {port} terpakai, tidak dapat melakukan test SDR",
            #         "data": {
            #             "Name":uname,
            #             "Port":port,
            #             "Time":time_processing,
            #             "Executed": "%s seconds" % (time.time() - start)
            #         }
            #     }
            
            return info
        except Exception as e:
            raise HTTPException(status_code=400, detail="Bad Request")
    
    # RTN
    def upload(self, terminal_id, uname, ip_tr, ip_server, port, time_processing):

        start = time.time()
        print(type(terminal_id))
        try:
            date = datetime.now()
            date = (date - timedelta(hours=7)).strftime('%Y-%m-%d %H:%M:%S')
            # date = date.replace(microsecond=0)
            # print(type(date))
            # print(type(time_processing))
            fwd = "FWD"
            conn = self.cfx.connectDB()
            # cursor = conn.cursor(dictionary=True)
            # query = f"""INSERT INTO iperf.log_kratos (terminal_id,start_datetime,duration, fwd_rtn_selection) 
            #             VALUES('{terminal_id}','{date}','{time_processing}','{fwd}') """
            # cursor.execute(query)
            # conn.commit()
            # conn.close()
            # return "OK"
            
            # uri = self.cfx.config['URL_SNT']
            # url = uri+"/api/server/statusport"

            # payload={}
            # headers = {}

            # response = requests.request("GET", url, headers=headers, data=payload)
            # data = response.json()
            # df = pd.DataFrame(data)
            # # print(df)
            
            # df = df.loc[df['ip']==ip_tr]
            # val = df['status_port'].values[0]
       
            # if val=='listen':
            #     print("jalankan")
            try:

                subprocess.Popen(f"ssh {uname}@{ip_tr} -i ~/.ssh/id_rsa iperf3 -c {ip_server} -u -b 23M -p {port} -t {time_processing} -R > /dev/null 2>/dev/null &",
                                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

                return {
                    "status": "200",
                    "data": {
                        "Name":uname,
                        "Port":port,
                        "Time":time_processing,
                        "Executed": "%s seconds" % (time.time() - start)
                    }
                }
            except Exception as e:
                 raise HTTPException(status_code=400, detail="Bad Request")
            # date = datetime.now()
            # date = date.replace(microsecond=0)
                # conn = self.cfx.connectDB()
                # cursor = conn.cursor(dictionary=True)
                # query = f"""INSERT INTO iperf.log_kratos (terminal_id,start_datetime,duration, fwd_rtn_selection) 
                #         VALUES('{terminal_id}','{date}','{time_processing}','FWD' """
                # cursor.execute(query)
                # conn.commit()
                # conn.close()
            #     return info
            # else:
            #     info = {
            #         "status": f"Port {port} terpakai, tidak dapat melakukan test SDR",
            #         "data": {
            #             "Name":uname,
            #             "Port":port,
            #             "Time":time_processing,
            #             "Executed": "%s seconds" % (time.time() - start)
            #         }
            #     }
            return info
        except Exception as e:
            raise HTTPException(status_code=400, detail="Bad Request")

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
        
    # minion for mini list
    def get_sites_status_on(self):
        try:
            
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            # query = """SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, (s.ip)as ip_server , 
            #             sites.port_server, sites.status ,sites.updated_at 
            #             from iperf.sites
            #             left join iperf.servers s on sites.ip_server = s.id """
            query = """SELECT sites.id, sites.subscriber_number, sites.name, sites.ip, sites.ip_server , 
                        sites.port_server, sites.status , status_port,sites.updated_at 
                        from iperf.sites """
            cursor.execute(query)
            data = cursor.fetchall()
            # conn.close()
            df = pd.DataFrame(data)
            # print(df)
            status = df['status']
            st = []
            for i in range(len(df['status'])):
                t = df['status'][i]
                if t == 1:
                    st.append("Active")
                else:
                    st.append("Not Active")
            # return st
            df['status'] = st
            
            # # # status port
            # url = uri+"/api/server/statusport"

            # payload = {}
            # headers = {}

            # r = requests.request("GET", url, headers=headers, data=payload)
            # r = r.json()
            # print(r)
            # temp_statusport = []
            # for j in r:
            #     temp_statusport.append(j['status_port'])
            # df['status_port']=temp_statusport
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
            url = uri+"/api/server/statusport"

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
            url = uri+"/api/zabbix/status"

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
            url = "http://202.95.150.42/api/zabbix/status"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            res = response.json()
            # print(res)
            # return 9
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
                # query = f"""UPDATE iperf.sites 
                #             SET status = {status}
                #             WHERE ip='{ip}'"""
                query = f"""UPDATE iperf.sites 
                            SET status = 1
                            WHERE ip='{ip}'"""
                cursor.execute(query)
                conn.commit()
                # conn.close()
                # temp.append(ip)
            
            return temp

        except Exception as e:
            raise e
    
    def put_modem_status(self):
        try:
            now = datetime.now()
            now = now.replace(microsecond=0, second=0)
            now = now.strftime("%H:%M:%S")
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            
            # print(df)
            # return 9
            url = uri+"/api/zabbix/status2"
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            res = response.json()
            # print(res['name'])
            # val = res[0]['name']
            # split_values = val.split('(')
            # val2 = split_values[1].rstrip(')')
            # return val2
            ada = []
            gak = []
            for i in res:
                # print(i['name'])
                val = i['name']
                val = val.split('(')
                val = val[1].rstrip(')')
                
                status = i['lastvalue']
                print(status)
                query = f"""UPDATE iperf.sites 
                            SET modem_status = {status}
                            WHERE subscriber_number='{val}'"""
                
                cursor.execute(query)
                conn.commit()
                # conn.close()
                ada.append(val)
                
           
            
            return ada

        except Exception as e:
            raise e
        
    def put_tr_statusport(self):
        try:
            now = datetime.now()
            now = now.replace(microsecond=0, second=0)
            now = now.strftime("%H:%M:%S")
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            
            url = uri+"/api/server/statusport"
            # print(url)
            # return 9
            payload = {}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            res = response.json()
            # print(res)
            df = pd.DataFrame(res)
            # print(df['ip'])
            # print(df['lastvalue'])
            temp = []
            for i in range(len(df['ip'])):
                ip = df['ip'][i]
                print(ip)
                status_port = df['status_port'][i]
                # print(type(status_port))
            #     status = int(df['lastvalue'][i])
            #     print(status)

                query = f"""UPDATE iperf.sites 
                            SET status_port = '{status_port}'
                            WHERE ip='{ip}'"""
                
                cursor.execute(query)
                conn.commit()
            
            return datetime.now()

        except Exception as e:
            raise e


    # used for detil
    def get_single_sites(self, id):
        try:
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT a.id, a.subscriber_number, a.name, a.user,a.ip, a.ip_server, a.port_server,a.status,
                         a.duration ,a.updated_at 
                         from iperf.sites a
                         WHERE a.id = {id}"""
            # query = f"""SELECT a.id, a.subscriber_number, a.name, a.user,a.ip, (s.ip) as ip_server, a.port_server,a.status,
            #             a.duration ,a.updated_at 
            #             from iperf.sites a
            #             left join iperf.servers s on a.ip_server = s.id 
            #             WHERE a.id = {id}"""
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
            
            # url = uri+"/api/server/statusport"

            # payload = {}
            # headers = {}

            # r = requests.request("GET", url, headers=headers, data=payload)
            # r = r.json()
            # # print(r)
            # # print(ip)
            # temp_statusport = []
            # for j in r:
            #     if j['ip']==ip:
            #         temp_statusport.append(j['status_port'])
            #     else:
            #         pass
            # print(temp_statusport[0])
           
            return {
                "id": id_mini,
                "subscriber_number":sbc,
                "name":name,
                "user":user,
                "ip":ip,
                "ip_server":ip_server,
                "port_server":port_server,
                "status_port":"",
                "status":status,
                "duration":duration
            }
            
        except Exception as e:
            raise e
        
    def get_single_chart(self, id, state, start_date, end_date):
        # now = datetime.now()
        # now = now.strftime("%Y-%m-%d %H:%M:%S")
        try:
            start_date = str(start_date + " 00:00:00")
            end_date = str(end_date+" 23:59:59")
          
            st_timestamp = int(time.mktime(datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S").timetuple()))
            # print("st_timestamp", st_timestamp)
            dt_timestamp = int(time.mktime(datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").timetuple()))
            # print("end_date",dt_timestamp)
            
            uri = self.cfx.config['URL_SNT']
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""SELECT sites.id, sites.ip from iperf.sites WHERE id = {id}"""
            cursor.execute(query)
            data = cursor.fetchall()
            ip = data[0]['ip']
            conn.close()

            url = uri+"/api_jsonrpc.php"
            # print(url)
            # return 9
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
            print("token:",token)
            # return 9
            # get download id
            payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                    "output": ["itemid","key_","lastvalue","lastclock"],
                    "host" : ip,
                    "filter": {
                        "key_": ["net.if.in[\"eth1\"]","net.if.out[\"eth1\"]"]
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
            # print(data)
            download_id = data['result'][0]['itemid']
            upload_id = data['result'][1]['itemid']
            # print(result)
   
            if state=="download":
                # get history download
                payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": download_id,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "time_from": st_timestamp,
                    "time_till": dt_timestamp
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
                    val_do = (int(j['value']))/1048576
                # print(to)
                    temp_download.append(val_do)
                df = pd.DataFrame(res_download)
                temp_time = []
                for k in res_download:
                    cl = int(k['clock'])
                    to_obj = datetime.fromtimestamp(cl)-timedelta(hours=7)
                    # print(type(to_obj))
                    temp_time.append(to_obj)
                df['val_download']=temp_download
                df['time']=temp_time
                df = df.loc[:,('val_download', 'time')]
                return df.to_dict("records")
                
            elif state=="upload":
                # get history upload
                payload = json.dumps({
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 3,
                    "itemids": upload_id,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "time_from": st_timestamp,
                    "time_till": dt_timestamp
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
                # print(data_upload)
                temp_upload = []
                for k in res_upload:
                    val_up = (int(k['value']))/1048576
                # print(to)
                    temp_upload.append(val_up)
                temp_time = []
                for l in res_upload:
                    cl = int(l['clock'])
                    to_obj = datetime.fromtimestamp(cl)-timedelta(hours=7)
                #   # print(to_obj)
                    temp_time.append(to_obj)
                df = pd.DataFrame(res_upload)
                df['val_upload']=temp_upload
                df['time']=temp_time
                df = df.loc[:,('val_upload', 'time')]
                return df.to_dict("records")
            else:
                return {"There's no state selected"}

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
            query = f"""SELECT a.sites_id as id, DATE_FORMAT(a.timee, '%H:%i:%s')as timee, a.tipe, a.duration 
                        FROM iperf.scheduler a LEFT JOIN iperf.sites b 
                        ON a.sites_id = b.subscriber_number 
                        WHERE b.ip_modem is NOT NULL"""
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
            query = f"""SELECT (a.sites_id) as id , DATE_FORMAT(a.timee, '%H:%i:%s')as timee, a.tipe, a.duration 
                        FROM iperf.scheduler a LEFT JOIN iperf.sites b 
                        ON a.sites_id = b.subscriber_number
                        WHERE b.ip_modem is NOT NULL """
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
        # print(post.sites_id)
        # print(type(post.sites_id))
        
        # return 0
        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"""INSERT INTO iperf.scheduler (sites_id, tipe, timee, duration, date_created) 
                        VALUES ('{post.sites_id}', '{post.tipe}', '{post.timee}','{post.duration}','{now}')"""
            cursor.execute(query)
            # print(query)
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
    
    def data_log(self):

        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM iperf.log_kratos ORDER BY id DESC"
            cursor.execute(query)
            data = cursor.fetchall()
            conn.close()
            return data

        except Exception as e:
            raise e
        
    def recap_sdr(self):

        try:
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT s.id, s.hit_upload, s.hit_download, s.subscriber_number, s.val_download, s.val_upload, s.updated_at from iperf.sites s"
            cursor.execute(query)
            data = cursor.fetchall()
            df = pd.DataFrame(data)
            temp =[]
            for i in data:
                dt = str(i['updated_at'])
                # print(i)
                dt = datetime.fromisoformat(dt)
                dt = dt.strftime("%d/%m/%Y %H:%M:%S")
                temp.append(dt)
            df['updated_at']=temp
            df = df.loc[:,['id','hit_upload','hit_download','subscriber_number','val_download','val_upload','updated_at']]
            val = df.to_dict('records')
            # print(val)
            # print(data)
            conn.close()
            return val

        except Exception as e:
            raise e

    def reboot_pid(self, subsciber_number):
        print(subsciber_number)
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # uname = config[("UNAME")]
            # print(uname)
            # server
            srv = self.cfx.server()
            # print(srv['ip'])
            ip =srv['ip']
            uname = srv['uname']
            passwd = srv['passwd']
            # return 9
            conn = self.cfx.connectDB()
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT s.id, s.subscriber_number, s.port_server from iperf.sites s where s.subscriber_number = '{subsciber_number}'"
            cursor.execute(query)
            data = cursor.fetchall()
            print("port server", data[0]['port_server'])
            # return 9
            port = data[0]['port_server']
            ssh_client.connect(ip, username=uname, password=passwd)
            com_pid = f"sudo lsof -i :{port} | awk 'NR==2 {{print $2}}'"
            stdin, stdout, stderr = ssh_client.exec_command(com_pid)
            pid = stdout.read().decode().strip()
            print(pid)
            # return 9
            ssh_client.exec_command(f"sudo kill -9 {int(pid)}")
            exe ="kill "+pid
            time.sleep(10)
            ssh_client.exec_command(f"iperf3 -s -p {int(port)} -D")
            # print(com_kill,": executed")
            # print(com_up,": executed")
            com_pid2 = f"sudo lsof -i :{port} | awk 'NR==2 {{print $2}}'"
            stdin, stdout, stderr = ssh_client.exec_command(com_pid2)
            pid2 = stdout.read().decode().strip()
            print(pid2)
            ssh_client.close()
            # pid = con_pid.read().decode().strip()
            # print(pid)
            # command = f"sudo lsof -i :{port} | awk 'NR==2 {{print $2}}'"
            # stdin, stdout, stderr = ssh_client.exec_command(command)
            # pid = stdout.read().decode().strip()
            data = {
                "status":"successfully reload port",
                "old pid":pid,
                "new pid":pid2
            }
            return data
        except Exception as e:
            raise HTTPException(status_code=400, detail="Something went wrong")