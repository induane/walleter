"""Base58 Implementation."""
import logging

LOG = logging.getLogger(__name__)
LETTERS = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


def encode(n):
    """Return number as base64 string value."""
    encode = []
    if n < 0:
        return ''
    while n >= 58:
        remainder = n % 58
        encode.append(LETTERS[remainder])
        n = n / 58
    if n:
        encode.append(LETTERS[n])
    return ''.join(reversed(encode))


def decode(s):
    """Decode a base58 encoded string into an integer."""
    start = 0
    multiplier = 1
    for char in s[::-1]:
        start += multiplier * LETTERS.index(char)
        multiplier = multiplier * 58
    return start
