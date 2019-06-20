from threading import *
from socket import *
from glob import *
import os
import platform
import random
import datetime

SERVER_PORT = 7734

def send_request(request, server_host, server_port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((server_host, server_port))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print('\r\n' + response)
    sock.close()

def join(client_host, client_port, server_host, server_port):
    request = "JOIN P2P-CI/1.0\r\nHost: %s\r\nPort: %s" % (client_host, client_port)
    send_request(request, server_host, server_port)

def add_rfc(client_host, client_port, server_host, server_port):
    print('Enter an RFC Number: ')
    rfc_number = input()
    print('Enter an RFC title: ')
    rfc_title = input()
    request = "ADD RFC %s P2P-CI/1.0\r\nHost: %s\r\nPort: %s\r\nTitle: %s\r\n" % (rfc_number, client_host,
                                                                                  client_port, rfc_title)
    # Create the file locally if it does not already exist
    with open('%s.txt' % rfc_number, 'w+') as f:
        f.write(rfc_title)
        f.close()
    send_request(request, server_host, server_port)

def list_rfcs(client_host, client_port, server_host, server_port):
    request = "LIST P2P-CI/1.0\r\nHost: %s\r\nPort: %s" % (client_host, client_port)
    send_request(request, server_host, server_port)

def lookup(client_host, client_port, server_host, server_port):
    print('Enter the RFC number you wish to find: ')
    rfc_num = input()
    # print('Enter the RFC title you wish to find: ')
    # rfc_title = input()
    request = 'LOOKUP RFC %s P2P-CI/1.0\r\nHost: %s\r\nPort: %s' % (rfc_num, client_host, client_port)
    send_request(request, server_host, server_port)

def peer_connection(peer_sock):
    request = peer_sock.recv(1024).decode()
    rfc_num = request.split('\r\n')[0].split(' ')[2]
    # P2P-CI/1.0 200 OK
    # Date: Wed, 12 Feb 2009 15:12:05 GMT 
    # OS: Mac OS 10.2.1
    # Last-Modified: Thu, 21 Jan 2001 9:23:46 GMT
    # Content-Length: 12345
    # Content-Type: text/text
    # (data data data ...)

    file_name = rfc_num + '.txt'
    if os.path.isfile(file_name):
        date = str(datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"))
        last_modified = str(os.stat(file_name).st_mtime)
        client_os = platform.system()
        file_size = os.path.getsize(file_name)
        message = 'P2P-CI/1.0 200 OK\r\nDate: %s\r\nOS: %s\r\nLast Modified: %s\r\nContent-Length: %s\r\nContent-Type: text/plain\r\n' % (date, last_modified, client_os, file_size)
        with open('%s.txt' % rfc_num, 'r') as f:
            file_content = f.readlines()
            for line in file_content:
                message += line
            f.close()  
        peer_sock.send(message.encode())
        peer_sock.close()
    else:
        message = 'P2P-CI/1.0 404 NOT_FOUND\r\n'
        peer_sock.send(message.encode())
        peer_sock.close()

def upload_server(client_port):
    client_sock = socket(AF_INET, SOCK_STREAM)
    client_sock.bind(('', int(client_port)))
    client_sock.listen(1)
    while True:
        (peer_sock, peer_host) = client_sock.accept()
        print('\r\nConnection received from %s\r\n' % str(peer_host))
        th = Thread(target=peer_connection,args=(peer_sock,))
        th.start()
        th.join()
    client_sock.close()

def send_peer_request(request, peer_host, peer_port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((peer_host, peer_port))
    sock.send(request.encode())
    response = sock.recv(1024).decode()
    print('Response from peer:\r\n%s' % response)

def get_rfc(client_host, client_port):
    print('Enter the RFC Number you would like to download: ')
    rfc_num = input()
    print('Enter the peer hostname you would like to download the RFC from: ')
    peer_host = input()
    print('Enter the peer port you would like to download the RFC form: ')
    peer_port = int(input())
    request = 'GET RFC %s P2P-CI/1.0\r\nHost: %s\r\nOS: %s' % (rfc_num, peer_host, platform.system())
    send_peer_request(request, peer_host, peer_port)

def notify_server_about_files(client_host, client_port, server_host, server_port):
    files = glob('*.txt')
    for filename in files:
        rfc_num = filename.split('.')[0]
        with open('%s.txt' % rfc_num, 'r') as f:
            rfc_title = f.readline()
            request = "ADD RFC %s P2P-CI/1.0\r\nHost: %s\r\nPort: %s\r\nTitle: %s\r\n" % (rfc_num, client_host,
                                                                                          client_port, rfc_title)
            send_request(request, server_host, server_port)
            f.close()

def main():
    
    client_host = input('Enter a unique hostname: ')
    while client_host == '':
      print('This value is required. Please try again.')
      client_host = input('Enter a unique hostname:' )
        
    while True:
        client_port = input('Enter a unique port number (between 1024-65535): ')
        try:
            if int(client_port) < 1024 or int(client_port) > 65535:
                print('Client port must be between 1024 and 65535. Please try again.')
                continue
            else:
                break
        except ValueError:
            print('Port number must be an integer. Please try again.')
            continue

    server_host = input('Enter hostname of central server: ')
    while server_host == '':
      print('This value is required. Please try again.')
      server_host = input('Enter hostname of central server: ')
    server_port = SERVER_PORT

    upload_thread = Thread(target=upload_server,args=(client_port,))
    # End thread when quitting.
    upload_thread.daemon = True
    upload_thread.start()

    join(client_host, client_port, server_host, server_port)
    notify_server_about_files(client_host, client_port, server_host, server_port)
    while True:
        try:
            print('Enter the command you would like to run (ADD, GET, LIST, LOOKUP, QUIT): ')
            user_input = input()
            if user_input.lower() == 'add':
                add_rfc(client_host, client_port, server_host, server_port)
            elif user_input.lower() == 'get':
                get_rfc(client_host, client_port)
            elif user_input.lower() == 'list':
                list_rfcs(client_host, client_port, server_host, server_port)
            elif user_input.lower() == 'lookup':
                lookup(client_host, client_port, server_host, server_port)
            elif user_input.lower() == 'quit':
                print('Exiting.')
                exit(0)
            else:
                print("P2P-CI/1.0 400 Bad Request\r\n")
                print("Invalid command. Please try again.\r\n")
                continue
        except Exception as e:
            print('Error occured: ' + str(e))
            continue
        
if __name__ == "__main__":
    main()
