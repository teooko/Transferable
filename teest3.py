import paramiko
from stat import S_ISDIR, S_ISREG
ssh_client = paramiko.SSHClient()
ssh_client.load_host_keys('hostkeys.txt')
#ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy())
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh_client.load_host_keys('C:/Users/teobo/Desktop/proiect/remote/test2/hostkeys.txt')
ssh_client.connect(hostname='127.0.0.1', username='teo',password='4156',port=22)
sftp_client=ssh_client.open_sftp()
path = "C:\Python\Python39"
for entry in sftp_client.listdir_attr(path):
    mode = entry.st_mode
    if S_ISDIR(mode):
        
        print(entry.filename)
        print(entry.st_size)
        print(entry.longname)
        print(entry.FLAG_PERMISSIONS)
        print(entry.st_uid)
    elif S_ISREG(mode):
        print(entry.filename + " is file")