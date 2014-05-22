#!/usr/bin/python
import sys

from lib.Server.CounterRequestHandler import CounterRequestHandler
from lib.Server.ThreadingTCPServer import ThreadingTCPServer
from lib.Server.Connection import DEFAULT


__author__ = 'nessvm'

"""This module is the server implementation for vote storage and count,
    it will have 2 network procedures:

    1 - Waiting for a connection from the voter and storing the received
    blinding factor.

    2 - Waiting for a connection from the vote validation authority, the
    counter will receive the blinded vote, and will unblind it for count.

    For the time being, this will be stored in memory.
    """


def main():
    # Creating server
    host = sys.argv[1]
    port = DEFAULT['ctr_port']
    server = ThreadingTCPServer(
        (host, port),
        CounterRequestHandler
    )

    server.serve_forever()


if __name__ == '__main__':
    main()