__author__ = 'nessvm'

from SocketServer import StreamRequestHandler
import socket
import time

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from lib.Server.Connection import DEFAULT


class ValidatorRequestHandler(StreamRequestHandler):
    def handle(self):
        data = self.rfile.read()

        # Creating decipher object with Validator private key
        f = open('../vtr.prv', 'r')
        key = RSA.importKey(f.read())
        decipher = PKCS1_v1_5.new(key)
        f.close()

        # Creating cipher object with Counter public key
        f = open('../ctr.pub', 'r')
        key = RSA.importKey(f.read())
        cipher = PKCS1_v1_5.new(key)
        f.close()

        if data[0] == '2':
            time.sleep(1)
            cipher_vote = decipher.decrypt(data[65:], None)
            print 'Type: Voter cast'
            print 'Data: {}'.format(str(cipher_vote))

            # Processing the ciphered vote and sending to the counter
            frame = str()
            frame += '3'
            frame += data[1:65]
            frame += cipher.encrypt(cipher_vote)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((DEFAULT['ctr_host'], DEFAULT['ctr_port']))
            sock.send(frame)
            sock.close()

        else:
            print 'Invalid frame'

        self.finish()