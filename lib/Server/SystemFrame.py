__author__ = 'nessvm'
import struct
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random


class SystemFrame:
    def __init__(self, frame):
        frame = bytearray(frame)
        # System frame types will always be the first byte on each frame
        self.type = frame[0]
        # Ciphertext size for the decipher, packed in 4 bytes.
        self.ct_size = struct.unpack('>I', bytes(frame[1:5]))[0]
        # Frame slots from 2 to 7 are currently unused
        self.us = frame[5:8]
        # Frame ID will be a SHA512 digest, so 512 bits -> 64 bytes
        self.id = frame[8:73]
        # Finally the frame data will be on the rest of the system frame
        self.data = frame[73: 73 + self.ct_size]
        print(self.data)

    def blind_sign(self, key):
        """ Perform a blind signature on a vote, received from a  caster
        using the complementary private RSA key to the  public  key  the
        caster should have used  to  send  the message,  the new data is
        written directly into the object  changing  the  type  attribute
        accordingly, leaving the object ready to be sent to the  Counter

        Keyword arguments:
        key - The RSA key object obtained with the  Crypto.PublicKey.RSA
        module
        """
        cipher = PKCS1_v1_5.new(key)
        sentinel = Random.new().read(len(self.data))
        self.data = cipher.decrypt(self.data, sentinel)
        self.type = VALIDATOR_SIG

    def process_vote(self, r):
        pass

    def to_bytes(self):
        return bytes(bytearray([self.type]) + self.us + self.id + self.data)

    def decrypt_data(self, key):
        decipher = PKCS1_v1_5.new(key)
        sentinel = Random.new().read(72)
        return decipher.decrypt(self.data[:self.ct_size], sentinel)


CASTER_RANDOM = 1  # Caster random number
CASTER_VOTE = 2  # Caster blinded vote
VALIDATOR_SIG = 3  # Validator signed blinded vote