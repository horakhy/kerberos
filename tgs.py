import pickle
import socket
import random
import string
import time

from component_util import decryptAES, encryptAES, get_server_key, parse_message

HOST = '127.0.0.1'
PORT = 8082

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen()

print(f'Server listening on {HOST}:{PORT}')

# Accept incoming connections and handle them
def build_fourth_message(K_C_TGS: bytes, ID_C: str, N_2: str):
    K_C_S = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16)) 
    T_A = time.time()

    K_S = get_server_key("service")
    K_S = K_S.encode()

    buffer_1 = f"{K_C_S},{T_A},{N_2}"
    T_C_S = f"{ID_C},{T_A},{K_C_S}"
    return [encryptAES(buffer_1, K_C_TGS), encryptAES(T_C_S, K_S)]

def send_fourth_message(conn, M_4: str):
    M_4_SERIALIZED = pickle.dumps(M_4)
    time.sleep(5)
    print("M_4 enviada ao cliente!")
    conn.sendall(M_4_SERIALIZED)

while True:
    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')

    with conn:
        while True:
            M_3_DATA = conn.recv(1024)
            if not M_3_DATA:
                break  
            
            print("M_3 foi recebida do Cliente!")
            
            M_3 = pickle.loads(M_3_DATA)
            TGS_KEY = get_server_key("tgs")
            TGS_KEY = TGS_KEY.encode()

            M_3_2 = decryptAES(M_3[1], TGS_KEY) 
            M_3_2 = parse_message(M_3_2)

            K_C_TGS = M_3_2[2] 
            K_C_TGS = K_C_TGS.encode()

            M_3_1 = decryptAES(M_3[0], K_C_TGS) 
            M_3_1 = parse_message(M_3_1)

            ID_C = M_3_1[0]
            T_R = M_3_1[2]
            N_2 = M_3_1[3]

            M_4 = build_fourth_message(K_C_TGS, ID_C, N_2)

            send_fourth_message(conn, M_4)

    print(f'Connection with {addr} closed')