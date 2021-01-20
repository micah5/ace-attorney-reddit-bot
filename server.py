import socket

IP = 'localhost'
PORT = 8080

# opens a server on IP, PORT and listens for a get request. parses the get request and then closes the server.
def get_request(IP, PORT):
    # creating the socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # binding the socket to IP, PORT and set it to listen
    server_socket.bind((IP, PORT))
    server_socket.listen()

    # while it hasn't recieved any messages, listen for messages.
    message = None
    while not message:
        # accept any incoming messages
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        message = client_socket.recv(4096).decode('ascii')
        print('message recieved')

    # after a message has been recieved, close the server.
    server_socket.close()

    # parses the get request to find what it's trying to "GET"
    for line in message.split('\n'):
        if 'GET' in line:
            request = line
            break

    return request.split(' ')[1]


if __name__ == '__main__':
    get_request(IP, PORT)
