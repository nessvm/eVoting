#! usr/bin/python
import socket
import time
import struct

from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from lib.Server.Connection import DEFAULT
from lib.Server.SystemFrame import SystemFrame


__author__ = 'nessvm'


def main():
    ctr_f = open('../ctr.pub', 'r')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DEFAULT['ctr_host'], DEFAULT['ctr_port']))

    t = time.localtime()
    hs = SHA512.new()
    hs.update(bytes(t[0]) + bytes(t[1]) + bytes(t[2]))
    ctr_key = RSA.importKey(ctr_f.read())
    cipher = PKCS1_v1_5.new(ctr_key)

    frame = bytearray()
    frame.append(1)
    frame += bytearray([0, 0, 0, 0])
    frame += bytearray([0]*3)
    frame += bytearray(hs.digest())
    ciphertext = cipher.encrypt(b'hola')
    print(ciphertext)
    frame += bytearray(ciphertext)
    frame = frame.replace(bytearray([0, 0, 0, 0]),
                  bytearray(struct.pack('>I', len(ciphertext))), 1)
    vote = SystemFrame(frame)

    sock.send(vote.to_bytes())


if __name__ == '__main__':
    main()