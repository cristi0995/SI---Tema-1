import socket
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Util.Padding import pad
import json

PORT = 1222
HOST = '127.0.0.1'
cbc_key = "8x/A?D*G-KaPdSgV"
ecb_key = get_random_bytes(16)
primeKey = b'abcdefgh12345678'
IV = b'security = swell'

def refreshed_key(encryption_key):
    return AES.new(encryption_key.encode(), AES.MODE_ECB).encrypt(primeKey)

def encrypt_key(key):
    data = b"secret"
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    print(key)
    print(result)
    return result

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
        x = refreshed_key(cbc_key)
        clientA.send(x)