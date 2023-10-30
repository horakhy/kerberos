import pickle
import socket
import time

from component_util import decryptAES, encryptAES, get_server_key, parse_message

HOST = '127.0.0.1'
PORT = 8083

# Create a socket using IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

server_socket.listen()

print(f'Service Server listening on {HOST}:{PORT}')

while True:
    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')

    
    with conn:
        while True:
            M_5_DATA = conn.recv(1024)
            if not M_5_DATA:
                break  
            
            M_5 = pickle.loads(M_5_DATA)

            HTTP_STATUS = "200"

            K_S = get_server_key("service")
            K_S = K_S.encode()

            M_5_2 = decryptAES(M_5[1], K_S)
            M_5_2 = parse_message(M_5_2)
           
            K_C_S = M_5_2[2]
            K_C_S = K_C_S.encode()

            M_5_1 = decryptAES(M_5[0], K_C_S)
            M_5_1 = parse_message(M_5_1)

            ID_C = M_5_1[0]
            T_A = M_5_1[1]
            S_R = M_5_1[2]
            N_3 = M_5_1[3]

            if S_R == "login":
                response = f"Ticket validado para {str(ID_C)}"
            if time.time() > float(T_A):
                response = "408"

            buffer = f"{response},{N_3}"

            M_6 = [encryptAES(buffer, K_C_S)]
            M_6_SERIALIZED = pickle.dumps(M_6)

            print("\nM_6 enviado ao cliente!\n")
            
            conn.sendall(M_6_SERIALIZED)

    print(f'Connection with {addr} closed')