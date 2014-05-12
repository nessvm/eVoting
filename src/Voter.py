#! usr/bin/python
import socket

from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto import Random

from lib.Server.Connection import DEFAULT


__author__ = 'nessvm'


def main():
    ctr_f = open('../ctr.pub', 'r')  # Public Counter RSA key file
    vtr_f = open('../vtr.pub', 'r')  # Public Validator RSA key file
    aes_f = Random.new()  # Random file-like object for generating an AES key

    sock = dict()  # CTR and VTR sockets dictionary
    cipher = dict()  # CTR and VTR ciphers dictionary
    # Counter socket creation
    sock['ctr'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock['ctr'].connect((DEFAULT['ctr_host'], DEFAULT['ctr_port']))
    # Validator socket creation
    sock['vtr'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock['vtr'].connect((DEFAULT['vtr_host'], DEFAULT['vtr_port']))

    key = dict()  # Keyring dictionary
    key['ctr'] = RSA.importKey(ctr_f.read())  # Counter key import
    key['vtr'] = RSA.importKey(vtr_f.read())  # Validator key import
    key['aes'] = aes_f.read(32)
    #TODO Verify CTR and VTR PKCS object creation (May be causing decryption error in VTR handle)

    cipher['ctr'] = PKCS1_v1_5.new(key['ctr'])  # Cipher object
    cipher['vtr'] = PKCS1_v1_5.new(key['vtr'])  # Cipher object
    # AES Cipher
    IV = aes_f.read(16)
    cipher['aes'] = AES.new(key['aes'], AES.MODE_CBC, IV)

    # Parameter input
    candidate = raw_input('Candidate\'s name: ')  # Vote input
    candidate = candidate.center(32, '*')
    cipher_candidate = cipher['aes'].encrypt(candidate)  # Encrypting vote with AES

    # User data is directly hashed, not stored
    hasher = SHA512.new(candidate + raw_input('Voter number: '))
    vote_id = hasher.digest()

    # Building the frame that will be sent to the Counter
    ctr_frame = bytes()
    ctr_frame += '1'  # Frame type [0]
    ctr_frame += vote_id  # ID [1:65]
    ctr_frame += IV  # AES IV [65:81]
    ctr_frame += cipher['ctr'].encrypt(key['aes'])  # Key [81:]

    # Building the frame that will be sent to the Validator
    vtr_frame = bytes()
    vtr_frame += '2'  # Frame type [0]
    vtr_frame += vote_id  # ID [1:65]
    vtr_frame += cipher['vtr'].encrypt(cipher_candidate)  # CT [65:]

    # Send the data
    sock['ctr'].send(ctr_frame)
    sock['vtr'].send(vtr_frame)

    sock['ctr'].close()
    sock['vtr'].close()


if __name__ == '__main__':
    main()