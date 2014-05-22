#!/usr/bin/python
import sys

from lib.Server.ValidatorRequestHandler import ValidatorRequestHandler
from lib.Server.ThreadingTCPServer import ThreadingTCPServer
from lib.Server.Connection import DEFAULT


__author__ = 'nessvm'


def main():
    # Creating server
    host = sys.argv[1]
    port = DEFAULT['vtr_port']
    server = ThreadingTCPServer(
        (host, port),
        ValidatorRequestHandler
    )
    server.serve_forever()


if __name__ == '__main__':
    main()
