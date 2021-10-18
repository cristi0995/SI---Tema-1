import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


PORT = 1222
HOST = '127.0.0.1'
cbc_key = "8u/A?D*G-KaPdSgV"
ecb_key = get_random_bytes(16)
primeKey = "abcdefgh12345678"
IV = b'security = swell'

def encrypt_key(plaintext):
    return AES.new(primeKey.encode('utf-8'), AES.MODE_ECB).encrypt(plaintext.encode('utf-8'))

def ECB(key):
    return str(key)

def CBC(key):
    return str(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(100)
msg = ''

while True:
    clientA, address = s.accept()
    print('S-a connectat clientul \'A\' !')
    print('Waiting...')
    msg = clientA.recv(1024)
    print(msg)
    if msg == 'ECB':
        clientA.send(bytes(encrypt_key(ecb_key),'UTF-8'))
    else:
        print(f'Key:           {cbc_key}')
        x = encrypt_key(cbc_key)
        print(f'Encrypted_key: {x}')
        clientA.send(x)