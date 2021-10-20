import os

path = __file__
path = path.replace("\\","\\\\")

os.system(f"powershell.exe Start-Process {path} -Verb RunAs")
