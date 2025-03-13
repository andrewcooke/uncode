from re import sub


# the type of the ciphertext (Guess.code) is not fixed; it only has to be a sequence
# of some values (with Guess.__encode and Guess.__decode mapping these values from
# and to characters).

# the parser converts the input string to the ciphertext type; the formatter converts
# it back to string for display.


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