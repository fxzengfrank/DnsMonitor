#! /usr/bin/env python
#! _*_ coding:utf-8 _*_

import logging, traceback, sys, os
import socket, json
import threading, time

NAME = "dnsmc"
VERSION = 20180709001

logging.basicConfig(level = logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(NAME)

class agent_thread(threading.Thread):
    def __init__(self, sock):
        super(agent_thread, self).__init__()
        self.daemon = True
        self.sock = sock
        self.sockf = sock.makefile(mode="rw")
    #
    def run(self):
        try:
            (p_addr, p_port) = self.sock.getpeername()
            logger.info("Client {0}:{1} connected".format(p_addr, p_port))
            sockf = self.sock.makefile(mode="rw")
            while True:
                b = sockf.readline()
                assert len(b) > 0
                logger.debug("Client {0}:{1} msg {2}".format(p_addr, p_port, b))
                msg = json.loads(b)
                if msg['type'] == 'hello':
                    pass
        except AssertionError:
            pass
        except:
            logger.debug(traceback.format_exc())
        finally:
            self.sock.close()
            logger.info("Client {0}:{1} disconnected".format(p_addr, p_port))
#
class controller():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", 9008))
    #
    def __call__(self):
        logger.info("Controller running..")
        logger.info("PID {0}".format(os.getpid()))
        (l_addr, l_port) = self.sock.getsockname()
        logger.info("Listen {0}:{1}".format(l_addr, l_port))
        self.sock.listen(5)
        while True:
            try:
                c_sock, c_addr = self.sock.accept()
                agent_thread(c_sock).start()
            except KeyboardInterrupt:
                print("\rKeyboardInterrupt")
                sys.exit(0)
            except:
                logger.debug(traceback.format_exc())
    #
#
if __name__ == "__main__":
    app = controller()
    app()
#
