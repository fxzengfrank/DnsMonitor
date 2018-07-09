#! /usr/bin/env python
#! _*_ coding:utf-8 _*_

import logging, traceback, sys
import socket, json
import threading, time

import env

NAME = "dnsma"
VERSION = 20180709001
RECONNECT_DELAY = 10

logging.basicConfig(level = logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(NAME)

class agent():
    def __init__(self):
        self.p_addr = ("127.0.0.1", 9008)
        logger.info("Initialized")
    #
    def __call__(self):
        while True:
            try:
                logger.info("Prepare to connect {0}:{1}".format(self.p_addr[0], self.p_addr[1]))
                sock = socket.socket()
                sock.connect(self.p_addr)
                (p_addr, p_port) = sock.getpeername()
                logger.info("Connected to {0}:{1}".format(p_addr, p_port))
                sockf = sock.makefile(mode="rw")
                self.hello(sockf)
                while True:
                    b = sockf.readline()
                    assert len(b) > 0
            except KeyboardInterrupt:
                print("\rKeyboardInterrupt")
                sys.exit(0)
            except:
                sock.close()
                logger.info("Not connected")
                logger.info("Waiting {0} seconds to reconnect".format(RECONNECT_DELAY))
                time.sleep(RECONNECT_DELAY)
    #
    def hello(self, sockf):
        msg = dict()
        msg['type'] = 'hello'
        msg['name'] = NAME
        msg['version'] = VERSION
        msg['sys.platform'] = env.get_sys_platform()
        msg['sys.version'] = env.get_sys_version()
        msg['os.uname'] = env.get_os_uname()
        sockf.write("{0}\n".format(json.dumps(msg)))
        sockf.flush()
#
if __name__ == "__main__":
    app = agent()
    app()
#
