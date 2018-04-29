def powershell_base64(data):
    """
    Encode something compatible for Powershell base64-encoding
    @zc00l
    """
    out = ""
    for char in data:
        out += char + "\x00"
    return out.encode("base64").replace("\n", "")