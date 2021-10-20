import os

path = __file__
path = path.replace("\\","\\\\")

os.system(f"Start-Process {path} -Verb RunAs")
