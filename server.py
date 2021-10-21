import socket
from Crypto.Cipher import AES


PORT = 1222
HOST = '127.0.0.1'
key = "8u/A?D*G-KaPdSgV"
primeKey = "abcdefgh12345678"


def encrypt_key(plaintext):
    return AES.new(primeKey.encode('utf-8'), AES.MODE_ECB).encrypt(plaintext.encode('utf-8'))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(100)
msg = ''

while True:
    clientA, address = s.accept()
    print('S-a connectat clientul \'A\' !')
    print('In asteptare...')
    msg = clientA.recv(100)
    print(msg)
    if msg == 'ECB':
        clientA.send(bytes(encrypt_key(key),'UTF-8'))
    else:
        print(f'Cheia:           {key}')
        x = encrypt_key(key)
        print(f'Cheia criptata:  {x}')
        clientA.send(x)