import socket

HOST = '127.0.0.1'
PORT = 8082

# Create a socket using IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen()

print(f'Service Server listening on {HOST}:{PORT}')

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

            # Handle the received data (e.g., echo it back)
            conn.sendall(data)

    print(f'Connection with {addr} closed')