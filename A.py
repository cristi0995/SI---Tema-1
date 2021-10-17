import socket

PORT1 = 1222
PORT2 = 1223
HOST = '127.0.0.1'
primeKey = 'abcdefgh12345678'


def ECB_encrypt(msg, key):
    return str(msg) #TO DO

def CBC_encrypt(msg, key):
    return str(msg) #TO DO

def encrypt(msg, type, key):
    if type == 'ECB':
        return ECB_encrypt(msg, key)
    return CBC_encrypt(msg, key)

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
key = keyManager.recv(1024)
print(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT2))
s.listen(100)
while True:
    B, address = s.accept()
    print('Conexiune realizata cu \'B\'!')
    B.send(bytes(key))
    B.send(bytes(type,'utf-8'))
    while True:
        msg = input('Introduceti mesaje: ')
        B.send(bytes(encrypt(msg, type, key), 'utf-8'))
