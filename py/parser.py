from base64 import b64decode, b64encode
from logging import getLogger
from re import sub

from utils import possibly_stdin

log = getLogger(__name__)


# the type of the ciphertext (Guess.code) is not fixed; it only has to be a sequence
# of some values (with Guess.__encode and Guess.__decode mapping these values from
# and to characters).

# the parser converts the input string to the ciphertext type; the formatter converts
# it back to string for display.


def string(code):
    return code


def string_fmt(code):
    return code


def hex(code):
    code = sub(r'\s+', '', code)
    return bytearray.fromhex(code)


def hex_fmt(code):
    return bytearray(code).hex()


def base64(code):
    return b64decode(code)


def base64_fmt(code):
    return b64encode(code).decode('ascii')


STRING = 'string'
HEX = 'hex'
BASE64 = 'base64'

PARSER = {
    STRING: string,
    HEX: hex,
    BASE64: base64
}

FMT = {
    STRING: string_fmt,
    HEX: hex_fmt,
    BASE64: base64_fmt
}


def read_code(code, format):
    code = possibly_stdin(code)
    parse, fmt = PARSER[format], FMT[format]
    code = parse(code)
    fmt_code = fmt(code)
    log.debug(f'code parsed to "{code}"')
    log.debug(f'which formats back to ({fmt_code})')
    return code, fmt_code
