from socket import *

SERVER_PORT = 7734

rfc_index = []
peers = []

class RFC:
    def __init__(self, number, title, host, port):
        self.number = number
        self.title = title
        self.host = host
        self.port = port

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

def join(request, client_socket):
    # Request format:
    # JOIN P2P-CI/1.0
    # Host: HELLO
    # Port: 12000
    host = request[1].split(':')[1]
    port = request[2].split(':')[1]
    curr_peer = Peer(host, port)
    peers.append(curr_peer)
    client_socket.send('Successfully connected to host.\r\n'.encode())

def add(request, client_socket):
    # Request format:
    # ADD RFC 123 P2P-CI/1.0
    # Host: thishost.csc.ncsu.edu
    # Port: 5678
    # Title: A Proferred Official ICP 
    rfc_number = request[0].split(' ')[2]
    rfc_title = request[3].split(':')[1]
    host = request[1].split(':')[1]
    port = request[2].split(':')[1]
    rfc = RFC(rfc_number, rfc_title, host, port)
    rfc_index.append(rfc)
    message = "P2P-CI/1.0 200 OK\r\nRFC%s %s %s %s\r\n" % (rfc_number, rfc_title, host, port)

    client_socket.send(message.encode())

def list_rfcs(request, client_socket):
    # Request format:
    # LIST ALL P2P-CI/1.0 
    # Host: thishost.csc.ncsu.edu 
    # Port: 5678
    host = request[1].split(':')[1]
    port = request[2].split(':')[1]
    phrase = request[0].split(' ')[1]
    if phrase.lower() == 'all':
        phrase = ''

    message = ''
    message += 'P2P-CI/1.0 200 OK %s\r\n' % phrase
    for rfc in rfc_index:
        if phrase.lower() in rfc.title.lower():
            message += 'RFC%s %s %s %s\r\n' % (rfc.number, rfc.title, host, port)
        else:
            message += '%s\r\n%s\r\n' % (phrase, rfc.title)
    client_socket.send(message.encode())

def lookup(request, client_socket):
    # Request format:
    # LOOKUP RFC 3457 P2P-CI/1.0
    # Host: thishost.csc.ncsu.edu
    # Port: 5678
    # Title: Requirements for IPsec Remote Access Scenarios
    req_rfc_num = request[0].split(' ')[2]
    rfc_found = False
    rfcs_matched = []
    for rfc in rfc_index:
        if req_rfc_num == rfc.number:
            rfc_found = True
            rfcs_matched.append(rfc)           
    if rfc_found:
        message = 'P2P-CI/1.0 200 OK\r\n'
        for rfc in rfcs_matched:
            message += 'RFC %s %s %s %s\r\n' % (rfc.number, rfc.title, rfc.host, rfc.port)
    else:
        message = 'P2P-CI/1.0 404 NOT_FOUND'
    client_socket.send(message.encode())

def main():
    server_port = SERVER_PORT
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(('', server_port))
    server_sock.listen(1)
    print('Awaiting connection.\r\n')
    while True:
        client_sock, client_addr = server_sock.accept()
        request = client_sock.recv(1024).decode()
        print(request + "\r\n")
        req_list = request.split('\r\n')
        if "JOIN" in req_list[0]:
            join(req_list, client_sock)
        elif "ADD" in req_list[0]:
            add(req_list, client_sock)
        elif "LIST" in req_list[0]:
            list_rfcs(req_list, client_sock)
        elif "LOOKUP" in req_list[0]:
            lookup(req_list, client_sock)
        else:
            error_msg = "P2P-CI/1.0 400 Bad Request\r\n"
            client_sock.send(error_msg.encode())
        client_sock.close()
    print('Exiting.\r\n')
    server_sock.close()

if __name__ == '__main__':
    main()
