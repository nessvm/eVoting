__author__ = 'nessvm'

from Crypto.Cipher import PKCS1_v1_5 as PKCS
from Crypto.PublicKey import RSA


def pubk_encrypt(key_path, data):
    key_file = open(key_path, 'r')  # Public RSA key file
    cipher = PKCS.new(RSA.importKey(key_file.read()))  # PKCS object
    key_file.close()

    return cipher.encrypt(data)