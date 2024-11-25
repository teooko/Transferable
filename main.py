import paramiko
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()
HOSTNAME = os.getenv('HOSTNAME')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

ssh_client = paramiko.SSHClient()
ssh_client.load_host_keys('hostkeys.txt')

#ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy())
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh_client.connect(hostname=HOSTNAME, username=USERNAME,password=PASSWORD,port=22)
sftp_client=ssh_client.open_sftp()

class Item:
    def __init__(self, mode, lastdate, lasthour, apm, length, name):
        self.mode = mode
        self.lastdate = lastdate
        self.lasthour = lasthour
        self.apm = apm
        self.length = length
        self.name = name


def addItems(com, count):

  item = []
  
  for i in range(7,count+7):
    spl = com[i]
    spl = ' '.join(spl.split())
    spl = spl.split(' ')
    mode = spl[0]
    lastdate = spl[1]
    lasthour = spl[2]

    apm = spl[3]
    if mode[0] == 'd':
      length = "0000"
      name = spl[4]
      j=5
      while len(spl) > j:
        name = name + " " + spl[j]
        j+=1
    else:
      length = spl[4]
      name = spl[5]
      j=6
      while len(spl) > j:
        name = name + " " + spl[j]
        j+=1
    item.append(Item(mode, lastdate, lasthour, apm, length, name))
  
  return item

def printItems(item):
  for i in range(count):
    print( str(i) + ". " + item[i].mode + " " + item[i].lastdate + " " + item[i].lasthour + " " + item[i].apm + " " + str(item[i].length) + " " + item[i].name)


def getItemNumber(path):
  stdin, stdout, stderr = ssh_client.exec_command('powershell -command "cd \'' + path + '\'; (Get-ChildItem | Measure-Object).Count"')
  st = int(stdout.read().decode("utf8"))
  stdin.close()
  stdout.close()
  stderr.close()
  return st

def getItemList(path):
  stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path \'' + path + '\'"')
  st = stdout.read().decode("utf8")
  print(st)
  stdin.close()
  stdout.close()
  stderr.close()
  
  return st

def downFolder(fcpath, fspath):
  count = getItemNumber(fspath)
  com = getItemList(fspath)
  com = com.split('\n')
  item = addItems(com, count)
  for i in range(count):
    if(item[i].mode[0] == 'd'):
      folder = i
      fspath2 = fspath + "/" + item[folder].name
      fcpath2 = fcpath + "/" + item[folder].name
      subprocess.Popen('powershell.exe New-Item -Path \'' + fcpath2 + '\' -ItemType Directory')
      downFolder(fcpath2, fspath2)
    else:
      sftp_client.get(fspath + "/" + item[i].name,fcpath + "/" + item[i].name)
    
def upFolder(fcpath, fspath):

  #UPDATE
  count = getItemNumber(fspath)
  com = getItemList(fspath)
  com = com.split('\n')
  item = addItems(com, count)
  for i in range(count):
    if(item[i].mode[0] == 'd'):
      folder = i
      fspath2 = fspath + "/" + item[folder].name
      fcpath2 = fcpath + "/" + item[folder].name
      stdin, stdout, stderr = ssh_client.exec_command('powershell -command "New-Item -Path \'' + fspath2 + '\' -ItemType Directory"')
      stdin.close()
      stdout.close()
      stderr.close()
      upFolder(fcpath2, fspath2)
    else:
      sftp_client.put(fcpath + "/" + item[i].name,fspath + "/" + item[i].name)

def moveFolder(foldpath, fnewpath):
  count = getItemNumber(foldpath)
  com = getItemList(foldpath)
  com = com.split('\n')
  item = addItems(com, count)
  for i in range(count):
    if(item[i].mode[0] == 'd'):
      folder = i
      fnewpath2 = fnewpath + "/" + item[folder].name
      foldpath2 = foldpath + "/" + item[folder].name
      stdin, stdout, stderr = ssh_client.exec_command('powershell -command "New-Item -Path \'' + fnewpath2 + '\' -ItemType Directory"')
      stdin.close()
      stdout.close()
      stderr.close()
      moveFolder(foldpath2, fnewpath2)
    else:
      sftp_client.rename(foldpath + "/" + item[i].name, fnewpath + "/" + item[i].name)
      
def removeFolder(foldpath):
  count = getItemNumber(foldpath)
  com = getItemList(foldpath)
  com = com.split('\n')
  item = addItems(com, count)
  for i in range(count):
    if(item[i].mode[0] == 'd'):
      removeFolder(foldpath + "/" + item[i].name)
      sftp_client.rmdir(foldpath + "/" + item[i].name)
    else:
      itempath = foldpath + "/" + item[i].name
      sftp_client.remove(itempath)


path = "C:/"
count = getItemNumber(path)
com = getItemList(path)
com = com.split('\n')

item = addItems(com, count)
printItems(item)

cond = 1
while cond:
  print(" 1 - access parent directory \n 2 - access folder \n 3 - download file \n 4 - upload file \n 5 - download folder \n 6 - upload folder \n 7 - rename item \n 8 - remove file \n 9 - remove folder \n 10 - move file \n 11 - move folder \n 12 - create folder \n 13 - refresh \n 0 - close ")
  cond = int(input())
  if cond == 1:
    path = path.rsplit('/', 1) 
    path = path[0]
    count = getItemNumber(path)
    com = getItemList(path)
    com = com.split('\n')

    item = addItems(com, count)
              
    printItems(item)
  
  if cond == 2:
    print("choose folder: ")
    fold = int(input())
    path = path + "/" + item[fold].name
    count = getItemNumber(path)
    com = getItemList(path)
    print(path)
    com = com.split('\n')

    item = addItems(com, count)
              
    printItems(item)

  if cond == 3:
    print("choose file: ")
    file = int(input())
    fspath = path + "/" + item[file].name
    fcpath = "C:/Users/Teo/Desktop/test" + "/" + item[file].name
    sftp_client.get(fspath,fcpath)
    
  if cond == 4:
    print("choose file: ")
    file = int(input())
    fspath = path + "/" + item[file].name
    fcpath = "C:/Users/Teo/Desktop/test" + "/" + item[file].name
    sftp_client.put(fcpath,fspath)

  if cond == 5:
    print("choose folder: ")
    folder = int(input())
    fspath = path + "/" + item[folder].name
    fcpath = "C:/Users/Teo/Desktop/test" + "/" + item[folder].name
    subprocess.Popen('powershell.exe New-Item -Path \'' + fcpath + '\' -ItemType Directory')
    downFolder(fcpath, fspath)

  if cond == 6:

    print("choose folder: ")
    folder = int(input())
    fspath = path + "/" + item[folder].name
    fcpath = "C:/Users/Teo/Desktop/test" + "/" + item[folder].name
    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "New-Item -Path \'' + fspath + '\' -ItemType Directory"')
    stdin.close()
    stdout.close()
    stderr.close()
    upFolder(fcpath, fspath)

  if cond == 7:
    print("choose item: ")
    it = int(input())
    print("choose name: ")
    name = str(input())
    oldpath = path + "/" + item[it].name
    newpath = path + "/" + name
    print(oldpath)
    sftp_client.posix_rename(oldpath, newpath)
    item[it].name = name

  if cond == 8:
    print("choose file: ")
    file = int(input())
    rpath = path + "/" + item[file].name
    sftp_client.remove(rpath)

  if cond == 9:
      print("choose folder: ")
      folder = int(input())
      rpath = path + "/" + item[folder].name
      removeFolder(rpath)
      sftp_client.rmdir(rpath)
    
  if cond == 10:
    print("choose file: ")
    file = int(input())
    oldpath = path + "/" + item[file].name 
    filename = item[file].name
    cond2 = 1
    count = getItemNumber(path)
    com = getItemList(path)
    com = com.split('\n')

    item = addItems(com, count)
    printItems(item)
    while cond2:
      
      
      print("1 - choose folder \n 2 - access folder \n 3 - acces parent directory \n 0 - cancel")
      cond2 = int(input())
      if cond2 == 1:
        print("which folder: ")
        folder = int(input())
        newpath = path + "/" + item[folder].name + "/" + filename
        sftp_client.rename(oldpath, newpath)
        cond2 = 0

      if cond2 == 2:
        print("which folder: ")
        fold = int(input())
        path = path + "/" + item[fold].name
        count = getItemNumber(path)
        com = getItemList(path)
        com = com.split('\n')

        item = addItems(com, count)
                  
        printItems(item)

      if cond2 == 3:
        path = path.rsplit('/', 1) 
        path = path[0]
        count = getItemNumber(path)
        com = getItemList(path)
        com = com.split('\n')

        item = addItems(com, count)
                  
        printItems(item)
  if cond == 11:
    print("choose folder: ")
    fold = int(input())
    oldpath = path + "/" + item[fold].name 
    filename = item[fold].name
    cond2 = 1
    count = getItemNumber(path)
    com = getItemList(path)
    com = com.split('\n')

    item = addItems(com, count)
    printItems(item)
    while cond2:
      
      
      print("1 - choose folder \n 2 - access folder \n 3 - acces parent directory \n 0 - cancel")
      cond2 = int(input())
      if cond2 == 1:
        print("which folder: ")
        folder = int(input())
        newpath = path + "/" + item[folder].name + "/" + filename
        stdin, stdout, stderr = ssh_client.exec_command('powershell -command "New-Item -Path \'' + newpath + '\' -ItemType Directory"')
        stdin.close()
        stdout.close()
        stderr.close()
        moveFolder(oldpath, newpath)
        stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Remove-Item \'' + oldpath + '\' -Recurse"')
        stdin.close()
        stdout.close()
        stderr.close()
        cond2 = 0

      if cond2 == 2:
        print("which folder: ")
        fold = int(input())
        path = path + "/" + item[fold].name
        count = getItemNumber(path)
        com = getItemList(path)
        com = com.split('\n')

        item = addItems(com, count)
                  
        printItems(item)

      if cond2 == 3:
        path = path.rsplit('/', 1) 
        path = path[0]
        count = getItemNumber(path)
        com = getItemList(path)
        com = com.split('\n')

        item = addItems(com, count)
                  
        printItems(item)
        
  if cond == 12:
    
    print("name the folder: ")
    name = str(input())
    fspath = path + "/" + name
    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "New-Item -Path \'' + fspath + '\' -ItemType Directory"')
    stdin.close()
    stdout.close()
    stderr.close()
    count = getItemNumber(path)
    com = getItemList(path)
    com = com.split('\n')

    item = addItems(com, count)
    printItems(item)

  if cond == 13:
    count = getItemNumber(path)
    com = getItemList(path)
    com = com.split('\n')

    item = addItems(com, count)
    printItems(item)

sftp_client.close()
ssh_client.close()