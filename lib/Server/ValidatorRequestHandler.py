__author__ = 'nessvm'

from SocketServer import StreamRequestHandler

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class ValidatorRequestHandler(StreamRequestHandler):
    def handle(self):
        data = self.rfile.read()

        f = open('../ctr.prv', 'r')
        key = RSA.importKey(f.read())
        decipher = PKCS1_v1_5.new(key)

        if data[0] == '2':
            print 'Type: Voter cast'
            print 'Data: {}'.format(str(decipher.decrypt(data[65:], None)))
            #TODO Solve error in PKCS decryption of Voter's type 2 frame on Validator
