import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


PORT = 1223
HOST = '127.0.0.1'
primeKey = b'abcdefgh12345678'

def ECB_decrypt(msg, key):
    return msg

def CBC_decrypt(msg, key):
    return msg

def decrypt_key (encrypted_key):
    x = AES.new(primeKey, AES.MODE_ECB)
    return x.decrypt(encrypted_key)

def decrypt(msg, type, key):
    if type == 'ECB':
        return ECB_decrypt(msg, key)
    return CBC_decrypt(msg, key)

A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
A.connect((HOST, PORT))
key = A.recv(1024)
print(key)
type = A.recv(1024)
print(type)
print(decrypt_key(key))
while True:
    msg = A.recv(9999)
    print(decrypt(msg, type, key))