import time
import glob


session = input("Session ID :")

if session not in glob.glob("./data/*.*"):
    with open(f"./data/{session}",'a') as file:
        file.write('')

previous = ""

while True:
    with open(f"./data/{session}",'r') as file:
        data = file.read()
        if data!=previous:
            previous = data
            print(previous)
    time.sleep(5)
