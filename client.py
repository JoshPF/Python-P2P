import _thread as thread
from socket import *

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
    rfc_number = int(input())
    print('Enter an RFC title: ')
    rfc_title = input()
    request = "ADD RFC %d P2P-CI/1.0\r\nHost: %s\r\nPort: %d\r\nTitle: %s\r\n" % (rfc_number, client_host,
            client_port, rfc_title)
    send_request(request, server_host, server_port)

def list_rfcs(client_host, client_port, server_host, server_port):
    print('Enter a phrase to search for or ALL to list all RFCs: ')
    phrase = input()
    request = "LIST %s P2P-CI/1.0\r\nHost: %s\r\nPort: %d" % (phrase.upper(), client_host, client_port)
    send_request(request, server_host, server_port)

def lookup(client_host, client_port, server_host, server_port):
    print('Enter the RFC number you wish to find: ')
    rfc_num = input()
    print('Enter the RFC title you wish to find: ')
    rfc_title = input()
    request = 'LOOKUP RFC %s P2P-CI/1.0\r\nHost: %s\r\nPort: %s\r\nTitle: %s' % (rfc_num, client_host, client_port, rfc_title)
    send_request(request, server_host, server_port)


def main():
    client_host = input('Enter a unique hostname: ')
    client_port = int(input('Enter a unique port number: '))

    server_host = input('Enter hostname of central server: ')
    server_port = SERVER_PORT

    join(client_host, client_port, server_host, server_port)
    while True:
        print('Enter the command you would like to run (ADD, GET, LIST, LOOKUP, QUIT): ')
        user_input = input()
        if user_input.lower() == 'add':
            add_rfc(client_host, client_port, server_host, server_port)
        elif user_input.lower() == 'get':
            print('not implemented')
            exit(1)
        elif user_input.lower() == 'list':
            list_rfcs(client_host, client_port, server_host, server_port)
            exit(1)
        elif user_input.lower() == 'lookup':
            lookup(client_host, client_port, server_host, server_port)
            exit(1)
        elif user_input.lower() == 'quit':
            print('Exiting.')
            exit(0)
        else:
            print('Invalid command. Please try again.\r\n')
            continue
        
if __name__ == "__main__":
    main()
