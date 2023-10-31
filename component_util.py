import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from Crypto.Random import get_random_bytes

def create_user():
    user_login = input("Login: ") 
    user_password = input("Senha: ")
    user_password = hashlib.sha256(user_password.encode()).hexdigest() 

    with open("client_data.txt", "a+") as file:
        file.write(f'{user_login}:{user_password}\n')

def validate_user(user_login: str, user_password: str):
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest() 
    user_data = user_login + ":" + hashed_password

    with open("client_data.txt", "r") as file:
        for line in file:
            if user_data in line:
                print("\nUsuário Autenticado, enviando Mensagem 1...\n")
                return True
        
        print("\nUsuário inexistente!\n\n")
        return False
    
def get_user_password(user_login: str):

   with open('client_data.txt','r', newline='\n') as f:
        for line in f:
            user_data = line.strip().split(':')
            if len(user_data) == 2 and user_data[0] == user_login:
                password = user_data[1]
                return password
        return ""
   
def encrypt_AES(message: str, key: bytes):
    message = str(message)
    message = message.encode()
    padded_message = pad(message, AES.block_size)

    iv_val = get_random_bytes(16)
    cipher = AES.new(key[:32], AES.MODE_CBC, iv_val)
    encoded_message = cipher.encrypt(padded_message)
    return base64.b64encode(iv_val + encoded_message).decode()

def decrypt_AES(message: str, key: bytes):
    message = base64.b64decode(message)
    iv_val = message[:16]
    message = message[16:]

    cipher = AES.new(key[:32], AES.MODE_CBC, iv_val)
    decoded_message = cipher.decrypt(message)
    decoded_message = unpad(decoded_message, AES.block_size)
    return decoded_message.decode()

def parse_message(message: str):
    parsed_message = message.strip("'")
    parsed_message_list = parsed_message.split(",")
    return parsed_message_list

def get_server_key(server):
    with open(f'{server}_server_data.txt','r', newline='\n') as f:
        for line in f:
            components = line.strip().split(':')
            if len(components) == 1:
                key = components[0]
                return key
        return -1