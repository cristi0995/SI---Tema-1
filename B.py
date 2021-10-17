import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64decode
from Crypto.Util.Padding import unpad
import json

PORT = 1223
HOST = '127.0.0.1'
primeKey = b'abcdefgh12345678'

def ECB_decrypt(msg, key):
    return msg

def CBC_decrypt(msg, key):
    b64 = json.loads(msg)
    iv = b64decode(b64['iv'])
    ct = b64decode(b64['ciphertext'])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    print("The message was: ", pt)
    return pt

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
print(decrypt(key, type, primeKey))
while True:
    msg = A.recv(9999)
    print(decrypt(msg, type, key))