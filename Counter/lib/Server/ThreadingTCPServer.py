#! /usr/bin/python

__author__ = 'nessvm'

from SocketServer import *


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass