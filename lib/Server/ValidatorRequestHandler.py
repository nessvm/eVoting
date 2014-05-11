__author__ = 'nessvm'

from SocketServer import StreamRequestHandler

from Crypto.Hash import SHA512

from SystemFrame import SystemFrame


class ValidatorRequestHandler(StreamRequestHandler):

    def handle(self):
        data = self.request.recv(4096)
        frame = SystemFrame(data)
        hs = SHA512.new()
        hs.update(frame.data)
        self.request.send(hs.digest())

        if 1 <= frame.type <= 3:
            print 'Received frame on validator'
            print 'Type: %d\nid: %s\nData: %s' % \
                  (frame.type, frame.id, frame.data)
