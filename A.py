import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


PORT1 = 1222
PORT2 = 1223
HOST = '127.0.0.1'
primeKey = 'abcdefgh12345678'
IV = b'security = swell'

c = "8u/A?D*G-KaPdSgV"


def pad(s):
    i = 16
    while i < len(s):
        i += 16
    j = i - len(s)
    for k in range(j):
        s += '!'
    return s

def byte_xor(ba1, ba2):
    x = bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])
    return x

def decrypt_key (encrypted_key):
    x = AES.new(primeKey.encode('utf-8'), AES.MODE_ECB)
    return x.decrypt(encrypted_key)

def encrypt(msg, type, key):
    if type == 'ECB':
        return ECB_encrypt(msg, key)
    return CBC_encrypt(msg, key, IV)

def ECB_encrypt(input_bytes, key):
    input_bytes = pad(input_bytes)
    current_block = bytes(input_bytes[:16],'utf-8')

    encrypted = b''
    while len(input_bytes) > 0:
        encrypted_block = AES.new(key, AES.MODE_ECB).encrypt(current_block)
        encrypted += encrypted_block
        input_bytes = input_bytes[16:]
        current_block = bytes(input_bytes[:16],'utf-8')
    return encrypted


def CBC_encrypt(input_bytes, key, initial_iv):
    
    input_bytes = pad(input_bytes)
    current_block = bytes(input_bytes,'utf-8')[:16]
    cbc_iv = initial_iv
    encrypted = b''
    while len(input_bytes) > 0:
        encrypted_block = AES.new(key, AES.MODE_ECB).encrypt(\
            #AES.new(cbc_iv, AES.MODE_ECB).encrypt(current_block))
            byte_xor(cbc_iv,current_block))
        encrypted += encrypted_block

        input_bytes = input_bytes[16:]
        current_block = bytes(input_bytes[:16],'utf-8')
        cbc_iv = encrypted_block
    return encrypted

keyManager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
keyManager.connect((HOST, PORT1))
type=''
input1 = ''
while type=='':
    input1 = input('Introduceti modul de criptare (ECB/CBC): ')
    if input1.upper() == 'ECB':
        keyManager.send(bytes('ECB', 'utf-8'))
        print('ECB')
        type=input1.upper()
    elif input1.upper() == 'CBC':
        keyManager.send(bytes('CBC', 'utf-8'))
        print('CBC')
        type=input1.upper()
    else:
        print('Comanda incorecta, incercati din nou!')
encrypted_key = keyManager.recv(16)
key = decrypt_key(encrypted_key)
print(f'Cheia criptata: {encrypted_key}')
print(f'Cheia:          {key}')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT2))
s.listen(100)
while True:
    B, address = s.accept()
    print('Conexiune realizata cu \'B\'!')
    B.send(bytes(encrypted_key))
    B.send(bytes(type,'utf-8'))
    while True:
        msg = input('Introduceti mesaje: ')
        B.send(encrypt(msg, type, key))
