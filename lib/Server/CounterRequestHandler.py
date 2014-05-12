__author__ = 'nessvm'

from SocketServer import StreamRequestHandler

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES


class CounterRequestHandler(StreamRequestHandler):
    """
    This class inherits from the default stream socket request  handler,
    it only overrides the handle() method for inbound requests, its  job
    is to decrypt the Caster's random number and create a new  entry  in
    memory for storing it and later on unblind the Caster's vote  signed
    by the Validator and count it.
    """


    def handle(self):
        data = self.rfile.read()

        f = open('../ctr.prv', 'r')
        key = RSA.importKey(f.read())
        decipher = PKCS1_v1_5.new(key)

        if data[0] == '1':
            aes_key = decipher.decrypt(data[81:], None)
            IV = data[65:81]
            print 'Type: Voter AES key'
            print 'Data: {}'.format(str())

            AES.new(aes_key, AES.MODE_CBC, IV)
            #TODO Implement a database for data storage
            self.finish()

        elif data[0] == '3':
            print 'Type: Validator signature'
            print 'Data: {}'.format(str(decipher.decrypt(data[65:], None)))
            self.finish()

        else:
            print 'Invalid frame received'
            self.finish()

            # if frame.type != 1 and frame.type != 3:
            #     print('Received an invalid frame')
            # elif frame.type == 1:
            #     print 'Received caster random number'
            #     print 'Random: %d' % frame.decrypt_data(key)
            # elif frame.type == 3:
            #     print 'Received validator blind signed vote'
            #     print 'Vote: %s' % frame.decrypt_data(key)