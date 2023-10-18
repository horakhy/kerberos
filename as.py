import socket
import random

# Define the host and port
HOST = '127.0.0.1'
PORT = 8080

# Create a socket using IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f'Server listening on {HOST}:{PORT}')

# Accept incoming connections and handle them
while True:
    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')

    # Handle the connection
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Connection closed by the client

            receivedMessage = data.decode()
            print('Received login:', receivedMessage)
            # You can perform further actions based on the login and password

            # Respond to the client
            response = "Received login and password"
            conn.sendall(response.encode())

    print(f'Connection with {addr} closed')