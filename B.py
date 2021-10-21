import socket
from Crypto.Cipher import AES

PORT = 1223
HOST = '127.0.0.1'
primeKey = b'abcdefgh12345678'
IV = b'security == good'

def unpad(s):
    for i in s[-16:]:
        if i == '!':
            s = s[:-1]
    s = s[:-1]
    return s

def byte_xor(ba1, ba2):
    x = bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    return x

def decrypt_key (encrypted_key):
    return AES.new(primeKey, AES.MODE_ECB).decrypt(encrypted_key)

def decrypt(msg, type, key):
    if type == bytes('ECB', 'utf-8'):
        return ECB_decrypt(msg, key)
    return CBC_decrypt(msg, key)

def ECB_decrypt(input_bytes, key):
    result = b''
    current_block = input_bytes[:16]
    while len(input_bytes) > 0:
        plain_text = AES.new(key, AES.MODE_ECB).decrypt(current_block)
        result += plain_text
        input_bytes = input_bytes[16:]
        current_block = input_bytes[:16]
    return unpad(str(result))

def CBC_decrypt(input_bytes, key):
    current_block = input_bytes[:16]
    iv = IV

    result = b''
    while len(input_bytes) > 0:
        plain_text = byte_xor(iv, AES.new(key, AES.MODE_ECB).decrypt(current_block))
        result += plain_text
        input_bytes = input_bytes[16:]
        iv = current_block
        current_block = input_bytes[:16]
    return unpad(str(result))



A = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
A.connect((HOST, PORT))
encrypted_key = A.recv(1024)
type = A.recv(1024)
print(f'Tipul de criptare:  {type}')
print(f'Cheia criptata: {encrypted_key}')
key = decrypt_key(encrypted_key)
print(f'Cheia:          {key}')
while True:
    msg = A.recv(9999)
    msg = decrypt(msg, type, key)
    print(msg)
    