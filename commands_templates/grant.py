import os

path = __file__
path = path.replace("\\","\\\\")

os.system(f"powershell.exe -exec bypass -WindowStyle Hidden Start-Process \"{path}\" -Verb RunAs")
