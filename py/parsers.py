from re import sub


def string(code):
    return list(code)


def string_fmt(code):
    return ''.join(code)


def hex(code):
    code = sub('\s+', '', code)
    return bytearray.fromhex(code)


def hex_fmt(code):
    return bytearray(code).hex()


STRING = 'string'
HEX = 'hex'

PARSER = {
    STRING: string,
    HEX: hex
}

FMT = {
    STRING: string_fmt,
    HEX: hex_fmt
}