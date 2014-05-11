__author__ = 'nessvm'

from SocketServer import StreamRequestHandler

from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA

from SystemFrame import SystemFrame


class CounterRequestHandler(StreamRequestHandler):
    """
    This class inherits from the default stream socket request  handler,
    it only overrides the handle() method for inbound requests, its  job
    is to decrypt the Caster's random number and create a new  entry  in
    memory for storing it and later on unblind the Caster's vote  signed
    by the Validator and count it.
    """
    #TODO Implement a hash table for vote storage
    #TODO Implement a database for vote storage

    def handle(self):
        data = self.request.recv(4096)
        frame = SystemFrame(data)
        hs = SHA512.new()
        hs.update(frame.data)
        self.request.send(hs.digest())

        f = open('../ctr.prv', 'r')
        key = RSA.importKey(f.read())

        if frame.type != 1 and frame.type != 3:
            print('Received an invalid frame')
        elif frame.type == 1:
            print 'Received caster random number'
            print 'Random: %d' % frame.decrypt_data(key)
        elif frame.type == 3:
            print 'Received validator blind signed vote'
            print 'Vote: %s' % frame.decrypt_data(key)