import socket
import random
import time
import pickle
import sys
from component_util import decrypt_AES, encrypt_AES, get_user_password, parse_message, validate_user
 
HOST = '127.0.0.1'
PORT = 8080
PORT_AS = 8081
PORT_TGS = 8082
PORT_SERVICE = 8083

ID_S = "server_id"
T_R = "60"

# M1 = [ID_C + {ID_S + T_R + N1}Kc]

# Create a socket using IPv4 and TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, 8085))
server_socket.listen()
print(f'Server listening on {HOST}:8085')

def menu():
    choice = input("1. Autenticar serviço\n")

    if choice == '1':
        user_login = input("Login: ") 
        user_password = input("Senha: ")
        
        if validate_user(user_login, user_password):
            client_server(user_login)
            return

    print("Escolha uma opção válida!")

def build_first_message(ID_C: bytes, N_1: bytes, K_C: bytes): 
    buffer_M1 = f"{ID_S},{T_R},{N_1}"
    return [ID_C, encrypt_AES(buffer_M1, K_C)]

def send_first_message(sock: socket, M_1: bytes):
    time.sleep(5)
    sock.connect((HOST, PORT_AS))
    serialized_M_1 = pickle.dumps(M_1)

    print("\nM1 enviada ao AS!\n")
    sock.sendall(serialized_M_1)

def build_third_message(ID_C: str, M_2, K_C_TGS: bytes):

    N_2 = '%08x' % random.getrandbits(32)
    T_C_TGS = M_2[1]

    buffer = f"{ID_C},{ID_S},{T_R},{N_2}"
    return [encrypt_AES(buffer, K_C_TGS), T_C_TGS]

def send_third_message(sock, M_3):
    time.sleep(5)
    sock.connect((HOST, PORT_TGS))
    M_3_SERIALIZED = pickle.dumps(M_3)

    sock.sendall(M_3_SERIALIZED)

def client_server(user_login: str):
    
    ID_C = user_login
    N_1 = '%08x' % random.getrandbits(32)
    K_C = get_user_password(user_login)

    K_C = K_C.encode()

    M_1 = build_first_message(ID_C, N_1, K_C)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        send_first_message(sock, M_1)

        M_2 = sock.recv(1024)
        M_2 = pickle.loads(M_2)

        print("M_2 recebida do AS!\n")
    
    M_2_DECRYPTED = decrypt_AES(M_2[0], K_C)
    M_2_DECRYPTED = parse_message(M_2_DECRYPTED)

    K_C_TGS = M_2_DECRYPTED[0]
    K_C_TGS = K_C_TGS.encode()

    M_3 = build_third_message(ID_C, M_2, K_C_TGS)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        send_third_message(sock, M_3)

        print("M_3 enviada ao servidor TGS!\n")

        M_4 = sock.recv(1024)
        M_4 = pickle.loads(M_4)
    
    M_4_DECRYPTED = decrypt_AES(M_4[0], K_C_TGS)
    M_4_DECRYPTED = parse_message(M_4_DECRYPTED)

    print("M_4 recebida do servidor TGS!\n")
        
    K_C_S = M_4_DECRYPTED[0]
    K_C_S = K_C_S.encode()

    T_A = M_4_DECRYPTED[1]
    S_R = "login"

    print(f"Data limite de acesso: {time.ctime(float(T_A))}\n")

    N_3 = '%08x' % random.getrandbits(32)

    T_C_S = M_4[1]

    buffer = f"{ID_C},{T_A},{S_R},{N_3}"

    M_5 = [encrypt_AES(buffer, K_C_S), T_C_S]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        time.sleep(5)
        sock.connect((HOST, PORT_SERVICE))
        M_5_SERIALIZED = pickle.dumps(M_5)

        while(True):
            sock.sendall(M_5_SERIALIZED)
            print("M_5 enviado ao Serviço\n")

            M_6 = sock.recv(1024)
            M_6 = pickle.loads(M_6)

            M_6_DECRYPTED = decrypt_AES(M_6[0], K_C_S)
            M_6_DECRYPTED = parse_message(M_6_DECRYPTED)

            print("M_6 recebido do Serviço\n")

            response = M_6_DECRYPTED[0]

            if(response == "408"):
                print("Ticket expirou!\n")
                sys.exit()
            else:
                print(response)
                print()
            time.sleep(10)




def main():
    menu()

if __name__ == "__main__":
    main()
