import paramiko
ssh_client = paramiko.SSHClient()
ssh_client.load_host_keys('hostkeys.txt')
#ssh_client.set_missing_host_key_policy(paramiko.RejectPolicy())
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh_client.load_host_keys('C:/Users/teobo/Desktop/proiect/remote/test2/hostkeys.txt')
ssh_client.connect(hostname='127.0.0.1', username='teo',password='4156',port=22)
sftp_client=ssh_client.open_sftp()

class Item:
    def __init__(self, mode, lastdate, lasthour, apm, length, name):
        self.mode = mode
        self.lastdate = lastdate
        self.lasthour = lasthour
        self.apm = apm
        self.length = length
        self.name = name

#path = input()  
#stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path ' + path + '"')

#com = stdout.read().decode("utf8")
#com = ' '.join(com.split())
#com = com.split(' ')
#for i in range(20):
#  print(com[i])
path = "C:\Python\Python39"
stdin, stdout, stderr = ssh_client.exec_command('powershell -command "cd "' + path + '"; (Get-ChildItem | Measure-Object).Count"')
count = int(stdout.read().decode("utf8"))

stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path ' + path + '"')
com = stdout.read().decode("utf8")


com = ' '.join(com.split())
com = com.split(' ')


item = []
j = 10
for i in range(count):
  
  mode = com[j+i]
  j+=1
  
  lastdate = com[j+i]
  j+=1
  
  lasthour = com[j+i]
  j+=1
   
  apm = com[j+i]
  
  if mode == "d-----":
    length = "0000"  
  else:
    j+=1
    length = com[j+i]
   
  j+=1
  
  
  name = com[j+i]
 
  item.append(Item(mode, lastdate, lasthour, apm, length, name))
      
i=0
for i in range(count):
  print( str(i) + ". " + item[i].mode + " " + item[i].lastdate + " " + item[i].lasthour + " " + item[i].apm + " " + str(item[i].length) + " " + item[i].name)










#-----------------------------------------------------------------------------------
cond = 1
while cond:
  print(" 1 - access parent directory \n 2 - access folder \n 0 - close ")
  cond = int(input())
  if cond == 1:
    path = path.rsplit('/', 1)
    path = path[0]
    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "cd "' + path + '"; (Get-ChildItem | Measure-Object).Count"')
    count = int(stdout.read().decode("utf8"))
    
    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path ' + path + '"')
    com = stdout.read().decode("utf8")
    
    com = ' '.join(com.split())
    com = com.split(' ')

    item = []
    j = 10
    for i in range(count):
      
      
      mode = com[j+i]
      j+=1
      
      
      lastdate = com[j+i]
      j+=1
      
      
      lasthour = com[j+i]
      j+=1
      
      
      apm = com[j+i]
      
      
    
      if mode == "d-----":
        length = "0000"
        
      else:
        j+=1
        length = com[j+i]
        
      j+=1
      
      
      name = com[j+i]
      item.append(Item(mode, lastdate, lasthour, apm, length, name))
          
    i=0
    for i in range(count):
      print( str(i) + ". " + item[i].mode + " " + item[i].lastdate + " " + item[i].lasthour + " " + item[i].apm + " " + str(item[i].length) + " " + item[i].name)




  
  if cond == 2:
    print("choose folder: ")
    fold = int(input())
    path = path + "/" + item[fold].name
    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "cd "' + path + '"; (Get-ChildItem | Measure-Object).Count"')
    count = int(stdout.read().decode("utf8"))
    
    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path ' + path + '"')
    com = stdout.read().decode("utf8")
    
    com = ' '.join(com.split())
    com = com.split(' ')

    item = []
    j = 10
    for i in range(count):
      
      
      mode = com[j+i]
      j+=1
      
      
      lastdate = com[j+i]
      j+=1
      
      
      lasthour = com[j+i]
      j+=1
      
      
      apm = com[j+i]
      
      
    
      if mode == "d-----":
        length = "0000"
        
      else:
        j+=1
        length = com[j+i]
        
      j+=1
      
      
      name = com[j+i]
      item.append(Item(mode, lastdate, lasthour, apm, length, name))
          
    i=0
    for i in range(count):
      print( str(i) + ". " + item[i].mode + " " + item[i].lastdate + " " + item[i].lasthour + " " + item[i].apm + " " + str(item[i].length) + " " + item[i].name)



#---------------------------------------------------------------------
  


  #  path = input()
  #  stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path ' + path + '"')

  #  print(f'STDOUT: {stdout.read().decode("utf8")}')
  #  print(f'STDERR: {stderr.read().decode("utf8")}')
    
   
#    print("1 for showing mother directory:")
 #   cond2 = int(input())
  #  if cond2:
   #     path = path.rsplit('/', 1)
    #    stdin, stdout, stderr = ssh_client.exec_command('powershell -command "Get-ChildItem -Path ' + path[0] + '"')
     #  
     #   print(f'STDOUT: {stdout.read().decode("utf8")}')
     #  print(f'STDERR: {stderr.read().decode("utf8")}')

   # print("1 for continue, 0 for closing:")
   # cond = int(input())

stdin.close()
stdout.close()
stderr.close()

sftp_client.close()
ssh_client.close()