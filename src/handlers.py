#!/usr/bin/env python2
# PTY, TCP_PTY_Handler classes were extracted from this URL
# https://github.com/infodox/python-pty-shells/blob/master/pty_shell_handler.py
# This is not officialy code from Shellpop project.

# The other classes, are.

from shellpop import *
from threading import Thread
from time import sleep
import termios
import select
import socket
import os
import fcntl
import sys

class PTY:
    def __init__(self, slave=0, pid=os.getpid()):
        # apparently python GC's modules before class instances so, here
        # we have some hax to ensure we can restore the terminal state.
        self.termios, self.fcntl = termios, fcntl

        # open our controlling PTY
        self.pty  = open(os.readlink("/proc/%d/fd/%d" % (pid, slave)), "rb+")

        # store our old termios settings so we can restore after
        # we are finished 
        self.oldtermios = termios.tcgetattr(self.pty)

        # get the current settings se we can modify them
        newattr = termios.tcgetattr(self.pty)

        # set the terminal to uncanonical mode and turn off
        # input echo.
        newattr[3] &= ~termios.ICANON & ~termios.ECHO

        # don't handle ^C / ^Z / ^\
        newattr[6][termios.VINTR] = '\x00'
        newattr[6][termios.VQUIT] = '\x00'
        newattr[6][termios.VSUSP] = '\x00'

        # set our new attributes
        termios.tcsetattr(self.pty, termios.TCSADRAIN, newattr)

        # store the old fcntl flags
        self.oldflags = fcntl.fcntl(self.pty, fcntl.F_GETFL)
        # fcntl.fcntl(self.pty, fcntl.F_SETFD, fcntl.FD_CLOEXEC)
        # make the PTY non-blocking
        fcntl.fcntl(self.pty, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

    def read(self, size=8192):
        return self.pty.read(size)

    def write(self, data):
        ret = self.pty.write(data)
        self.pty.flush()
        return ret

    def fileno(self):
        return self.pty.fileno()

    def __del__(self):
        # restore the terminal settings on deletion
        self.termios.tcsetattr(self.pty, self.termios.TCSAFLUSH, self.oldtermios)
        self.fcntl.fcntl(self.pty, self.fcntl.F_SETFL, self.oldflags)

class TCP_PTY_Handler(object):
    def __init__(self, addr, bind=True):
        self.bind = bind
        self.addr = addr

        if self.bind:
            self.sock = socket.socket()
            self.sock.bind(self.addr)
            self.sock.listen(5)

    def handle(self, addr=None):
        addr = addr or self.addr
        if self.bind is True:
            print(info("Waiting for connections ..."))
            sock, addr = self.sock.accept()
            print(info("Connection inbound from {0}:{1}".format(self.addr[0], self.addr[1])))
        else:
            sock = socket.socket()
            print(info("Waiting up to 10 seconds to start establishing the connection ..."))
            sleep(10)
            
            print(info("Connecting to remote endpoint ..."))
            n = 0
            while n < 10:
                try:
                    sock.connect(addr)
                    print(info("Connection to remote endpoint established."))
                    break
                except socket.error:
                    print(error("Connection could not be established."))
                    n += 1
                    sleep(5)


        # create our PTY
        pty = PTY()

        # input buffers for the fd's
        buffers = [ [ sock, [] ], [ pty, [] ] ]
        def buffer_index(fd):
            for index, buffer in enumerate(buffers):
                if buffer[0] == fd:
                    return index

        readable_fds = [ sock, pty ]

        data = " "
        # keep going until something deds
        while data:
            # if any of the fd's need to be written to, add them to the
            # writable_fds
            writable_fds = []
            for buffer in buffers:
                if buffer[1]:
                    writable_fds.append(buffer[0])

            r, w, x = select.select(readable_fds, writable_fds, [])

            # read from the fd's and store their input in the other fd's buffer
            for fd in r:
                buffer = buffers[buffer_index(fd) ^ 1][1]
                if hasattr(fd, "read"):
                    data = fd.read(8192)
                else:
                    data = fd.recv(8192)
                if data:
                    buffer.append(data)

            # send data from each buffer onto the proper FD
            for fd in w:
                buffer = buffers[buffer_index(fd)][1]
                data = buffer[0]
                if hasattr(fd, "write"):
                    fd.write(data)
                else:
                    fd.send(data)
                buffer.remove(data)

        # close the socket
        sock.close()

class TCP_Handler(object):
    """
    TCP handler class to get our shells!
    @zc00l
    """
    def __init__(self, conn_info, bind=True):
        self.conn_info = conn_info
        self.bind = bind
        self.sock = None

    @staticmethod
    def read_and_loop(sock):
        while True:
            try:
                data = sock.recv(1024)
                if data and len(data) > 0:
                    sys.stdout.write(data)
            except socket.timeout:
                sleep(1)
            except KeyboardInterrupt:
                sock.close()
                return 0
            except socket.error:
                print(error("Exiting shell handler ...."))
                sock.close()
                return 0

    @staticmethod
    def write_and_loop(sock):
        while True:
            try:
                s = raw_input("")
                if len(s) > 0:
                    sock.send(s+"\n")
                    if s.lower() == "exit":
                        raise KeyboardInterrupt # we want exit!
            except KeyboardInterrupt:
                sock.close()
                return 0
            except:
                pass

    def handle(self):
        sock = None
        self.sock = socket.socket()
        if self.bind is True:
            self.sock.bind(self.conn_info)
            self.sock.listen(5)

            sock, addr = self.sock.accept()
            print(info("Connection inbound from {0}:{1}".format(addr[0], addr[1])))
        else:  # reverse shell.
            print(info("Waiting up to 10 seconds to start establishing the connection ..."))
            sleep(10)

            print(info("Connecting to remote endpoint ..."))
            n = 0
            while n < 10:
                try:
                    self.sock.connect(self.conn_info)
                    sock = self.sock
                    print(info("Connection to remote endpoint established."))
                    break
                except socket.error:
                    print(error("Connection to remote endpoint could not be established."))
                    n += 1
                    sleep(4.5)

        if sock is None:  # we assume we have a connection by now.
            print(error("No connection socket to use."))
            exit(0)
        else:
            sock.settimeout(1.0)

        t = Thread(target=self.read_and_loop, args=(sock,))
        t.start()  # start the read in loop.
        t2 = Thread(target=self.write_and_loop, args=(sock,))
        t2.start()
        t.join()

def reverse_tcp_handler(conn_info):
    handler = TCP_Handler(conn_info, bind=True)
    handler.handle()

def bind_tcp_handler(conn_info):
    handler = TCP_Handler(conn_info, bind=False)
    handler.handle()

def reverse_tcp_pty_handler(conn_info):
    handler = TCP_PTY_Handler(conn_info, bind=True)
    handler.handle()

def bind_tcp_pty_handler(conn_info):
    handler = TCP_PTY_Handler(conn_info, bind=False)
    handler.handle()