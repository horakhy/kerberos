import socket
import pickle
import string
import random
import time

from component_util import create_user, decrypt_AES, encrypt_AES, get_server_key, get_user_password, parse_message

HOST = '127.0.0.1'
PORT = 8081

# Create a socket using IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f'Server listening on {HOST}:{PORT}')

# create_user()

def build_second_message(M_1: str, ID_C: str, K_C: bytes):
    decrypted_M_1 = decrypt_AES(M_1[1], K_C)
    decrypted_M_1 = parse_message(decrypted_M_1)
    ID_S = decrypted_M_1[0]
    T_R = decrypted_M_1[1]
    N_1 = decrypted_M_1[2]

    K_C_TGS = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))

    K_TGS = get_server_key("tgs")
    K_TGS = K_TGS.encode()

    buffer_1 = f"{K_C_TGS},{N_1}"
    buffer_2 = f"{ID_C},{T_R},{K_C_TGS}"
    M_2 = [encrypt_AES(buffer_1, K_C), encrypt_AES(buffer_2, K_TGS)]
    return M_2

def send_second_message(conn, M_2: str):
    M_2_SERIALIZED = pickle.dumps(M_2)
    time.sleep(5)
    
    print("M2 enviada ao Cliente")
    conn.sendall(M_2_SERIALIZED)

while True:
    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')

    with conn:
        while True:
            M_1_data = conn.recv(1024)
            if not M_1_data:
                break

            print("M_1 recebida do Cliente!\n")

            M_1 = pickle.loads(M_1_data)
            ID_C = M_1[0]
            K_C = get_user_password(ID_C)[:32]
            K_C = K_C.encode()

            M_2 = build_second_message(M_1, ID_C, K_C)
            send_second_message(conn, M_2)