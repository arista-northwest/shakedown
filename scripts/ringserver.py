#!/usr/bin/env python

import collections
import multiprocessing
import os
import random
import socket
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def handle(connection, address):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("process-%r" % (address,))
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)
            connection.sendall(data)
            logger.debug("Sent data")
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()

class Server(object):
    def __init__(self, address):
        self.logger = logging.getLogger("server")
        self.address = address

    def cleanup(self):
        try:
            os.unlink(self.address)
        except OSError:
            if os.path.exists(self.address):
                raise

    def start(self):
        self.cleanup()

        self.logger.debug("listening")
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            self.logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True

            process.start()

            self.logger.debug("Started process %r", process)

class RingServer(object):

    def __init__(self, maxlen=100, sockaddr='/tmp/ring_server.sock'):
        self._path = path
        self._maxlen = maxlen
        self._buff = collections.deque(maxlen=maxlen)
        self._server = Server(sockaddr)

    def __enter__(self):

        self._server.start()
        return self

    def __exit__(self, *args):
        #self._handle.close()
        pass

    def bind(self):
        pass


    def write(self, line):

        self._buff.append(line.strip() + "\n")

    #     self.flush()
    #
    # def flush(self):
    #     with open(self._path, 'w') as fh:
    #         for line in self._buffer:
    #             fh.write(line)

if __name__ == "__main__":
    path = './clogger.log'
    with RingServer() as buff:
        print "hi"
        # while True:
        #     timestamp = time.time()
        #     line = "{}: {}".format(timestamp, random.random())
        #     buff.write(line)
        #     time.sleep(.01)
