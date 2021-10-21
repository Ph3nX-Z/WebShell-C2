import os

path = __file__
path = path.split(".")[0]+".exe"
path = path.replace("\\","\\\\")

os.system(f"powershell.exe Start-Process {path} -Verb RunAs")
