from django.shortcuts import render,redirect
from django.contrib import messages
import paramiko
from .models import logfile
from django.http import HttpResponse
# Create your views here.
ftp = None
ssh_client = None
IP1 = 0
IP2 = 0
def ssh(request, ips = None):
  global ssh_client
  global ftp, IP1
  sys_messages = messages.get_messages(request)
  for message in sys_messages:
    pass
  sys_messages.used = True
  if request.method == 'POST':
    IP = request.POST.get('ip')
    IP1 = '10.48.193.54'
    if ips is None:
      ips = IP
    
    
    try:
      ssh_client = paramiko.SSHClient()
      username = "nutanix"
      password = "nutanix/4u"
      ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh_client.connect(hostname=IP1,username=username, password=password) 
      
    except:
      messages.info(request, 'Enter correct values')
    
  # return render(request,"index.html")

def index(request):
  logfile.objects.all().delete()
  ssh(request,IP1)
  # if ssh_client is not None:
  #   return redirect("/logs")
  
  return render(request,"index.html")

def main(request):
  # try:
  global IP2
  ssh(request,IP1)
  print(IP1)
  cmd= "sudo find /home/nutanix/data/logs -name '*.log'"
  stdin, stdout, stderr = ssh_client.exec_command(cmd)
  s = stdout.readlines()
  for i in range(len(s)):
    ab = logfile.objects.create(name = s[i])
    ab.save()
  files = logfile.objects.all()
  
  IP2 = IP1
  # except:
  #   pass
  #   return redirect("/")
  return render(request,'main.html',{"files":files})

def logout(request):
  return redirect("/")

def file(request):
  
  if request.POST:
    ssh(request,IP2)
    print(IP2)
    ids = request.POST.get("ss",False)
    names = logfile.objects.filter(id=ids)
    for n in names:
      print(n.name)
    with open('log.txt','r') as f:
      s = f.readlines()
      # print(s)

  return HttpResponse(s)
    
  # return render(request,"files.html")