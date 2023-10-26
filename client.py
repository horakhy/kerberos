import socket
import random
import time
import pickle

from component_util import encryptAES, get_user_password, validate_user
 
HOST = '127.0.0.1'
PORT = 8080
PORT_AS = 8081

ID_S = "server_id"
T_R = 60

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

    print("Escolha uma opção válida!")

def build_first_message(ID_C: bytes, N_1: bytes, K_C: bytes): 
    buffer_M1 = f"{ID_S},{T_R},{N_1}"
    return [ID_C, encryptAES(buffer_M1, K_C)]

def send_first_message(sock: socket, M_1: bytes):
    time.sleep(5)
    sock.connect((HOST, PORT_AS))
    serialized_M_1 = pickle.dumps(M_1)

    print("\n\nPrimeira mensagem enviada ao AS!!!\n\n")
    sock.sendall(serialized_M_1)

def client_server(user_login: str):
    
    ID_C = user_login
    N_1 = '%08x' % random.getrandbits(32)
    K_C = get_user_password(user_login)

    K_C = K_C.encode()

    M_1 = build_first_message(ID_C, N_1, K_C)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        send_first_message(sock, M_1)


def main():
    menu()

if __name__ == "__main__":
    main()
