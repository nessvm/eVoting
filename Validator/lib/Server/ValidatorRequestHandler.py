__author__ = 'nessvm'

from SocketServer import StreamRequestHandler
import socket

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from lib.Server.Connection import DEFAULT


class ValidatorRequestHandler(StreamRequestHandler):
    def handle(self):
        data = self.rfile.read()

        # Creating decipher object with Validator private key
        f = open('key/vtr.prv', 'r')
        key = RSA.importKey(f.read())
        decipher = PKCS1_v1_5.new(key)
        f.close()

        # Creating cipher object with Counter public key
        f = open('key/ctr.pub', 'r')
        key = RSA.importKey(f.read())
        cipher = PKCS1_v1_5.new(key)
        f.close()

        if data[0] == '2':
            cipher_vote = decipher.decrypt(data[65:], None)
            print 'Type: Voter cast'
            print 'Data: {}'.format(str(cipher_vote))

            # Reading the CTR address
            ip_file = open("ctr", "r")
            ctr_address = ip_file.read()
            ip_file.close()

            # Processing the ciphered vote and sending to the counter
            frame = str()
            frame += '3'
            frame += data[1:65]
            frame += cipher.encrypt(cipher_vote)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ctr_address, DEFAULT['ctr_port']))
            sock.send(frame)
            sock.close()

        elif data[0] == '4':
            print data
            ip_file = open("ctr", "w")
            ip_file.write(data[1:])
            ip_file.close()

        else:
            print 'Invalid frame'

        self.finish()