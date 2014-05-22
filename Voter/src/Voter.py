#! usr/bin/python
import socket
import sys

from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto import Random

from lib.Server.Security import pubk_encrypt
from lib.Server.Connection import DEFAULT


__author__ = 'nessvm'


def main():
    aes_f = Random.new()  # Random file-like object for generating an AES key

    sock = dict()  # CTR and VTR sockets dictionary
    # Counter socket creation
    sock['ctr'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock['ctr'].connect((sys.argv[1], DEFAULT['ctr_port']))
    # Validator socket creation
    sock['vtr'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock['vtr'].connect((sys.argv[2], DEFAULT['vtr_port']))
    # Validator address comm socket
    sock['ip'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock['ip'].connect((sys.argv[2], DEFAULT['vtr_port']))

    aes_key = aes_f.read(32)

    # AES Cipher
    IV = aes_f.read(16)  # Initialization Vector
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, IV)

    # Parameter input
    candidate = raw_input('Candidate\'s name: ')  # Vote input
    candidate = candidate.ljust(32)
    # User data is directly hashed, not stored
    hasher = SHA512.new(candidate + raw_input('Voter number: '))
    vote_id = hasher.digest()

    cipher_candidate = aes_cipher.encrypt(candidate)  # Encrypting vote with AES

    # Building the frame that will be sent to the Counter
    ctr_frame = bytes()
    ctr_frame += '1'  # Frame type [0]
    ctr_frame += vote_id  # ID [1:65]
    ctr_frame += IV  # AES IV [65:81]
    ctr_frame += pubk_encrypt('key/ctr.pub', aes_key)  # Key [81:]

    # Building the frame that will be sent to the Validator
    vtr_frame = bytes()
    vtr_frame += '2'  # Frame type [0]
    vtr_frame += vote_id  # ID [1:65]
    vtr_frame += pubk_encrypt('key/vtr.pub', cipher_candidate)  # CT [65 :]

    # Building the frame for sending a server the IP address of the other server
    ip_frame = bytes()
    ip_frame += '4'  # Frame type [0]
    ip_frame += sys.argv[1]  # TODO Correct major vulnerability

    # Send the data
    sock['ctr'].send(ctr_frame)
    sock['ip'].send(ip_frame)
    sock['vtr'].send(vtr_frame)

    sock['ctr'].close()
    sock['vtr'].close()
    sock['ip'].close()


if __name__ == '__main__':
    main()
