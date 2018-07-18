import os
import random
import re
import string

def randomize_vars(code, smallVars):
    nums = re.findall("NUM\d", code)
    vars = re.findall("VAR\d+", code)

    if smallVars:
        maxNum = 999
    else:
        maxNum = 9999999

    for num in nums:
        code = code.replace(num, str(random.randint(0, maxNum)))

    for var in vars:
        code = code.replace(var, gen_random_var(smallVars))

    return code

def gen_random_var(smallVars):
    if smallVars:
        minVarLen = 3
        maxVarLen = 6
    else:
        minVarLen = 6
        maxVarLen = 15

    randVarLen = 0
    while randVarLen < minVarLen:
        randVarLen = ord(os.urandom(1)) % (maxVarLen + 1)

    randomVar = "".join(string.ascii_letters[ord(os.urandom(1)) % 52] for x in range(randVarLen))

    return randomVar
    

def ipfuscate(ip, smallIP):
    """
    Obfuscate an IP address by converting it to decimal, hex, 
    octal, or a combination of the three.
    Code borrowed from @vysecurity (https://github.com/vysec/IPFuscator)
    Implemented by @capnspacehook
    """
    parts = ip.split('.')

    if not smallIP:
        ip = random_base_ip_gen(parts, smallIP)
        
    else:
        type = ord(os.urandom(1)) % 4
        decimal = int(parts[0]) * 16777216 + int(parts[1]) * 65536 + int(parts[2]) * 256 + int(parts[3])

        if type == 0:
            ip = decimal
        elif type == 1:
            ip = hex(decimal)
        elif type == 2:
            ip = oct(decimal)
        else:
            ip = random_base_ip_gen(parts, smallIP)

    return str(ip)

def random_base_ip_gen(parts, smallIP):
    """
    Used by ipfuscate(), returns an obfuscated IP with random bases.
    Code borrowed from @vysecurity (https://github.com/vysec/IPFuscator)
    Implemented by @capnspacehook
    """
    
    hexParts = []
    octParts = []

    for i in parts:
		hexParts.append(hex(int(i)))
		octParts.append(oct(int(i)))

    randBaseIP = ""
    baseChoices = []
    ip_obfuscated = False
    while not ip_obfuscated:
        for i in range(0,4):
            val = ord(os.urandom(1)) % 3
            baseChoices.append(val)
            if val == 0:
                # dec
                randBaseIP += parts[i] + '.'
            elif val == 1:
                # hex
                if not smallIP:
                    randBaseIP += hexParts[i].replace('0x', '0x' + '0' * (ord(os.urandom(1)) % 31)) + '.'
                else:
                    randBaseIP += hexParts[i] + '.'
            else:
                # oct
                if not smallIP:
                    randBaseIP += '0' * (ord(os.urandom(1)) % 31) + octParts[i] + '.'
                else:
                    randBaseIP += octParts[i] + '.'

        # Check to make sure all four parts of IP aren't decimal... in which case nothing would have changed
        if sum(baseChoices) > 0:
            ip_obfuscated = True
        else:
            baseChoices.clear()

    return randBaseIP[:-1]

def obfuscate_port(port, smallPort):
    """
    Obfuscate a port number by replacing the single int
    with an arithmetic expression. Returns a string that
    when evaluated mathmatically, is equal to the port entered.
    @capnspacehook 
    """
    modPieces = gen_mod_expr(port)

    if smallPort:
        return "(%s*%s+%s)" % (modPieces[0], modPieces[1], modPieces[2])
    else:
        portStr = ""
        portStrPieces = []
        for part in modPieces:
            if part != 0:
                choice = ord(os.urandom(1)) % 2
                if choice:
                    portStrPieces.append(gen_simple_expr(part))
                else:
                    part = gen_mod_expr(part)
                    portStrPieces.append("(%s*%s+%s)" % (part[0], part[1], part[2]))
            else:
                portStrPieces.append("0")

        return "(%s*%s+%s)" % (portStrPieces[0], portStrPieces[1], portStrPieces[2])
                
            
def gen_mod_expr(n):
    if n == 1:
        right = n
    else:
        right = random.randint(1, int(n / 2))
    left = int(n / right)
    remainder = n % right    
    
    return (left, right, remainder)

def gen_simple_expr(n):
    choice = ord(os.urandom(1)) % 3
    left = 0
    if choice == 0:
        left = random.randint(-n * 2, n - 1)
        right = random.randint(-n + 1, n * 2)
        if left + right < n:
            offset = n - (left + right)
            expr = "(%s+%s)--%s" % (left, right, offset)
        else:
            offset = (left + right) - n
            expr = "((%s+%s)-%s)" % (left, right, offset)
    elif choice == 1:
        left = random.randint(-n + 1, n * 2)
        right = random.randint(-n * 2, n + 1)
        if left - right < n:
            offset = n - (left - right)
            expr = "((%s-%s)--%s)" % (left, right, offset)
        else:
            offset = (left - right) - n
            expr = "((%s-%s)-%s)" % (left, right, offset)
    elif choice == 2:
        left = random.randint(2, int(n / 2) + 2)
        right = random.randint(int(n / 5), int(n / 3))
        if left * right < n:
            offset = n - (left * right)
            expr = "((%s*%s)--%s)" % (left, right, offset)
        else:
            offset = (left * right) - n
            expr = "((%s*%s)-%s)" % (left, right, offset)

    return expr
