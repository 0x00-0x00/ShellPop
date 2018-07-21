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
        if sum(baseChoices) > 4:
            ip_obfuscated = True
        else:
            randBaseIP = ""
            del baseChoices[:]

    return randBaseIP[:-1]

def obfuscate_port(port, smallExpr):
    """
    Obfuscate a port number by replacing the single int
    with an arithmetic expression. Returns a string that
    when evaluated mathmatically, is equal to the port entered.
    @capnspacehook 
    """
    exprStr, baseExprPieces = gen_simple_expr(port, smallExpr)

    if smallExpr:
        portExpr = exprStr % (baseExprPieces[0], baseExprPieces[1], baseExprPieces[2])
    else:
        subExprs = []
        for piece in baseExprPieces:
            expr, pieces = gen_simple_expr(piece, smallExpr)
            subExprs.append(expr % (pieces[0], pieces[1], pieces[2]))

        portExpr = exprStr % (subExprs[0], subExprs[1], subExprs[2])
        
    # Randomly replace '+' with '--'. Same thing, more confusing
    match = re.search("\+\d+", portExpr)
    beginingExprLen = 0
    while match is not None:   
        match = list(match.span())
        match[0] += beginingExprLen
        match[1] += beginingExprLen
        choice = ord(os.urandom(1)) % 2

        if choice:
            portExpr = portExpr[:match[0]] + "-(-" + portExpr[match[0] + 1:match[1]] + ")" + portExpr[match[1]:]

        beginingExprLen = len(portExpr[:match[1]])
        match = re.search("\+\d+", portExpr[match[1]:])
    
    # Properly separate any double '-' signs. Some langs complain
    match = re.search("--\d+", portExpr)
    beginingExprLen = 0
    while match is not None:   
        match = list(match.span())
        match[0] += beginingExprLen
        match[1] += beginingExprLen

        portExpr = portExpr[:match[0]] + "-(" + portExpr[match[0] + 1:match[1]] + ")" + portExpr[match[1]:]

        beginingExprLen = len(portExpr[:match[1]])
        match = re.search("--\d+", portExpr[match[1]:])
        
    return portExpr


def gen_simple_expr(n, smallExpr):
    """
    Generates a simple mathmatical expression of 3 terms
    that equal the number passed. Returns a template
    expression string, and a tuple of the values of the 
    terms in the generated expression.
    @capnspacehook
    """
    if type(n) == str:
        n = int(eval(n))

    if n == 0:
        N = 0
        while N == 0:
            N = random.randint(-99999, 99999)
    else:
        N = n

    choice = ord(os.urandom(1)) % 3
    left = 0
    if choice == 0:
        if N < 0:
            left = random.randint(N * 2, -N + 1)
            right = random.randint(N - 1, -N * 2)
        else:
            left = random.randint(-N * 2, N - 1)
            right = random.randint(-N + 1, N * 2)

        if left + right < n:
            offset = n - (left + right)
            expr = "((%s+%s)+%s)"
        else:
            offset = (left + right) - n
            expr = "(-(-(%s+%s)+%s))"
    elif choice == 1:
        if N < 0:
            left = random.randint(N - 1, -N * 2)
            right = random.randint(N * 2, N - 1)
        else:
            left = random.randint(-N + 1, N * 2)
            right = random.randint(-N * 2, N + 1)

        if left - right < n:
            offset = n - (left - right)
            expr = "((%s-%s)+%s)"
        else:
            offset = (left - right) - n
            expr = "(-(-(%s-%s)+%s))"
    elif choice == 2:
        if N < 0:
            left = random.randint(int(N / 2), -int(N / 2) - 2)
            right = random.randint(int(N / 3), -int(N / 3))
        else:
            left = random.randint(-int(n / 2), int(n / 2) + 2)
            right = random.randint(-int(n / 3), int(n / 3))

        if left * right < n:
            offset = n - (left * right)
            expr = "((%s*%s)+%s)"
        else:
            offset = (left * right) - n
            expr = "(-(-(%s*%s)+%s))"

    # Replace all zeros with an expression. Zeros make arithemetic easy
    if not smallExpr:
        if left == 0:
            zeroExpr, terms = gen_simple_expr(0, smallExpr)
            left = zeroExpr % (terms[0], terms[1], terms[2])
        if right == 0:
            zeroExpr, terms = gen_simple_expr(0, smallExpr)
            right = zeroExpr % (terms[0], terms[1], terms[2])
        if offset == 0:
            zeroExpr, terms = gen_simple_expr(0, smallExpr)
            offset = zeroExpr % (terms[0], terms[1], terms[2])

    return (expr, (left, right, offset))
