import socket
import hashlib
import random
from cryptography.fernet import Fernet
 
HOST = '127.0.0.1'
PORT = 8080

ID_C = "client_id"
ID_S = "server_id"
T_R = "60"
K_C = Fernet.generate_key()
N_1 = str(random.randint(1, 50))

# Create a socket using IPv4 and TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, 8085))
server_socket.listen()
print(f'Server listening on {HOST}:8085')

def menu():
    choice = input("1. Cadastrar usuário\n2. Autenticar servico\n")

    if choice == '1':
        user_login = input("Login: ") 
        user_password = input("Senha: ")
        user_data = user_login + ":" + hashlib.sha512(user_password.encode()).hexdigest() 

        with open("client_data.txt", "a") as file:
            file.write(user_data + "\n")
        return

    if choice == '2':
        client_server()
        return
    
    print("Escolha uma opção válida!")

def validateUser(user_login: str, user_password: str):
    hashed_password = hashlib.sha512(user_password.encode()).hexdigest() 
    user_data = user_login + ":" + hashed_password

    with open("client_data.txt", "r") as file:
        for line in file:
            if user_data in line:
                print("\nUsuário Autenticado, enviando Mensagem 1...\n")
                return
        
        print("\nUsuário inexistente!\n\n")
        menu()

def build_first_message(): 
    fernet = Fernet(K_C)
    return [ID_C, [fernet.encrypt(ID_S), fernet.encrypt(T_R), fernet.encrypt(N_1)]]

def client_server():
    try:
        client_socket.connect((HOST, PORT))

        user_login = input("Login: ") 
        user_password = input("Senha: ")

        validateUser(user_login, user_password)

        first_message = build_first_message()

        print(first_message)

        data = client_socket.recv(1024)
        print('Received from server:', data.decode())
    except ConnectionRefusedError:
        print('Connection refused. Make sure the server is running.')
    finally:
        # Close the socket
        client_socket.close()

while True:
    menu()

    conn, addr = server_socket.accept()
    print(f'Connected to {addr}')

    # Handle the connection
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break  # Connection closed by the client

        
            
    print(f'Connection with {addr} closed')


