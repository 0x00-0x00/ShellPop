from urllib import quote
from binascii import hexlify


def to_urlencode(data):
    """
    URL-encode a byte stream, plus some other characters that
    might be avoided by quote() from urllib.
    @zc00l
    """
    additional = [".", "/"]
    data = quote(data)
    for each in additional:
        data = data.replace(each, "%" + hexlify(each))
    return data


def to_unicode(data):
    """
    Get a string and make it Unicode
    @zc00l
    """
    out = ""
    for char in data:
        out += char + "\x00"
    return out


def powershell_base64(data, unicode_encoding=True):
    """
    Encode something compatible for Powershell base64-encoding
    Default behaviour is to encode Unicode before Base64.
    @zc00l
    """
    data = to_unicode(data) if unicode_encoding is True else data
    return data.encode("base64").replace("\n", "")


def xor(data, key):
    """
    XOR a byte-stream with a single key value (int)
    @zc00l
    """
    if type(key) is not int:
        return None
    output = ""
    for char in data:
        index = data.index(char)
        output += chr(ord(data[index]) ^ key)
    return output

