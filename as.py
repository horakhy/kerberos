import socket
import pickle

from component_util import create_user, decryptAES, get_user_password, parse_message

HOST = '127.0.0.1'
PORT = 8081

# Create a socket using IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f'Server listening on {HOST}:{PORT}')

create_user()

while True:
    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')

    with conn:
        while True:
            M_1_data = conn.recv(1024)
            if not M_1_data:
                break

            print("A primeira mensagem foi recebida do Cliente!\n")

            print("M1", M_1_data)
            M_1 = pickle.loads(M_1_data)
            ID_C = M_1[0]
            K_C = get_user_password(ID_C)[:32]
            K_C = K_C.encode()

            print("M1[1]", M_1[1])

            decrypted_M_1 = decryptAES(M_1[1], K_C)
            decrypted_M_1 = parse_message(decrypted_M_1)
            ID_S = decrypted_M_1[0]
            T_R = decrypted_M_1[1]
            N_1 = decrypted_M_1[2]

            print("ID_S ", ID_S)
            print("TR ", ID_S)
            print("N_1 ", ID_S)

            print(decrypted_M_1)

    print(f'Connection with {addr} closed')