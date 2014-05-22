__author__ = 'nessvm'

from SocketServer import StreamRequestHandler
import time

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Random import random

from lib.Database.DBVote import DBVote


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

        # Importing the RSA key and creating the PKCS object
        f = open('key/ctr.prv', 'r')
        key = RSA.importKey(f.read())
        decipher = PKCS1_v1_5.new(key)
        f.close()

        # Creating a connection to the database
        db = DBVote()

        if data[0] == '1':
            row = dict()  # The row to be inserted
            row['id'] = db.escape_bytea(data[1:65])
            row['aes_key'] = db.escape_bytea(decipher.decrypt(data[81:], None))
            row['iv'] = db.escape_bytea(data[65:81])
            db.insert('public."Vote"', row)
            print 'Type: Voter AES key'
            print 'Data: {}'.format(row['aes_key'])
            #TODO Implement the vote counting algorithm

        elif data[0] == '3':
            # RSA Decryption
            ciphertext = decipher.decrypt(data[65:], None)
            # Fetching AES parameters
            ID = db.escape_bytea(data[1:65])
            res = db.query('SELECT "Vote"."aes_key", "Vote"."iv" FROM public."Vote" WHERE ' +
                           '"Vote"."id"=\'{}\';'.format(ID))
            key = db.unescape_bytea(res.dictresult()[0]['aes_key'])
            iv = db.unescape_bytea(res.dictresult()[0]['iv'])
            # AES Decryption
            decipher = AES.new(key, AES.MODE_CBC, iv)
            candidate = decipher.decrypt(ciphertext).rstrip()
            # Database update
            # A random integer is generated to ensure vote confidentiality from frequent
            # database queries, set to a random delay between 15 seconds and 2 minutes
            delay = random.randint(15, 120)
            time.sleep(delay)

            row = dict()
            row['id'] = ID
            row['candidate'] = candidate
            db.update('public."Vote"', row)
            print 'Type: Validator signature'
            print 'Data: {}'.format(candidate)

        else:
            print 'Invalid frame received'

        db.close()
        self.finish()