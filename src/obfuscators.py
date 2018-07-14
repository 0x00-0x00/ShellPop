import os

def ipfuscate(ip, smallIP):
    """
    Obfuscate an IP address by converting it to decimal, hex, 
    octal, or a combination of the three.
    Code borrowed from @vysecurity (https://github.com/vysec/IPFuscator)
    Implemented by @capnspacehook
    """
    parts = ip.split('.')

    if not smallIP:
        ip = randomBaseIPgen(parts, smallIP)
        
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
            ip = randomBaseIPgen(parts, smallIP)

    return str(ip)

def randomBaseIPgen(parts, smallIP):
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
    for i in range(0,4):
        val = ord(os.urandom(1)) % 3
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

    return randBaseIP[:-1]
