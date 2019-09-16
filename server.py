from socket import *

SERVER_PORT = 7734

file_index = []
peers = []

class File:
    def __init__(self, title, host, port):
        self.title = title
        self.host = host
        self.port = port

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

def join(request, client_socket):
    # Request format:
    # JOIN Python-P2P/1.0
    # Host: HOST
    # Port: 12000
    host = request[1].split(':')[1]
    port = request[2].split(':')[1]
    curr_peer = Peer(host, port)
    peers.append(curr_peer)
    client_socket.send('Successfully connected to host.\r\n'.encode())

def add(request, client_socket):
    # Request format:
    # ADD FILE Python-P2P/1.0
    # Host: thishost.csc.ncsu.edu
    # Port: 5678
    # Title: filename.txt
    file_title = request[3].split(':')[1].strip()
    host = request[1].split(':')[1]
    port = request[2].split(':')[1]
    f = File(file_title, host, port)
    file_index.append(f)
    message = "Python-P2P/1.0 200 OK\r\n %s %s %s\r\n" % (file_title, host, port)

    client_socket.send(message.encode())

def list_files(request, client_socket):
    # Request format:
    # LIST ALL Python-P2P/1.0 
    # Host: thishost.csc.ncsu.edu 
    # Port: 5678
    host = request[1].split(':')[1]
    port = request[2].split(':')[1]
    message = 'Python-P2P/1.0 200 OK\r\n'
    for f in file_index:
        message += '%s %s %s\r\n' % (f.title, f.host, f.port)
    client_socket.send(message.encode())

def lookup(request, client_socket):
    # Request format:
    # LOOKUP FILE test.txt Python-P2P/1.0
    # Host: thishost.csc.ncsu.edu
    # Port: 5678
    # Title: Requirements for IPsec Remote Access Scenarios
    req_filename = request[0].split(' ')[2]
    file_found = False
    files_matched = []
    for f in file_index:
        if req_filename == f.title:
            file_found = True
            files_matched.append(f)           
    if file_found:
        message = 'Python-P2P/1.0 200 OK\r\n'
        for f in files_matched:
            message += '%s %s %s\r\n' % (f.title, f.host, f.port)
    else:
        message = 'Python-P2P/1.0 404 NOT_FOUND'
    client_socket.send(message.encode())

def main():
    server_host = gethostbyname(gethostname())
    print('Server started on %s:%d' % (server_host, SERVER_PORT))

    server_port = SERVER_PORT
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(('', server_port))
    server_sock.listen(5)
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
            list_files(req_list, client_sock)
        elif "LOOKUP" in req_list[0]:
            lookup(req_list, client_sock)
        else:
            error_msg = "Python-P2P 400 Bad Request\r\n"
            client_sock.send(error_msg.encode())
        client_sock.close()
    print('Exiting.\r\n')
    server_sock.close()

if __name__ == '__main__':
    main()
