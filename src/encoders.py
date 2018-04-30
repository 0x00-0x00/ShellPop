def powershell_base64(data):
    """
    Encode something compatible for Powershell base64-encoding
    @zc00l
    """
    out = ""
    for char in data:
        out += char + "\x00"
    return out.encode("base64").replace("\n", "")

def xor(data, key):
    """
    XOR a byte-stream with a single key value (int)
    """
    if type(key) is not int:
        return None
    output = ""
    for char in data:
        index = data.index(char)
        output += chr(data[index] ^ key)
    return output

