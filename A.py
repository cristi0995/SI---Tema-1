import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

PORT1 = 1222
PORT2 = 1223
HOST = '127.0.0.1'
primeKey = 'abcdefgh12345678'

c = "8u/A?D*G-KaPdSgV"

def encrypted_key(plaintext):
    return AES.new(plaintext.encode('utf-8'), AES.MODE_ECB).encrypt(primeKey.encode('utf-8'))

def ECB_encrypt(msg, key):
    return str(msg) #TO DO

def CBC_encrypt(msg, key):
    return str(msg) #TO DO

def encrypt(msg, type, key):
    if type == 'ECB':
        return ECB_encrypt(msg, key)
    return CBC_encrypt(msg, key)

def decrypt_key (encrypted_key):
    x = AES.new(primeKey.encode('utf-8'), AES.MODE_ECB)
    return x.decrypt(encrypted_key)

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
key = encrypted_key
key = decrypt_key(encrypted_key)
print(f'Encrypted_key: {encrypted_key}')
print(f'Key:           {key}\n')

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
        B.send(bytes(encrypt(msg, type, key), 'utf-8'))
