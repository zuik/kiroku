"""
ID generator
"""

ALPHABET = "abcdefghijklmnopqrstuvwxyz234567"


def to_b32(num_id):
    """
    From numerical id to base 32

    :param int num_id:
    :return: base_32 string
    """
    if num_id < 32:
        return ALPHABET[num_id]
    return to_b32(int(num_id / 32)) + ALPHABET[(num_id % 32)]


def from_b32(b32_text):
    """
    From base 32 id to numerical id

    :param str b32_text:
    :return: int numerical id
    """

    return sum([ALPHABET.index(n) * 32 ** i for i, n in enumerate(b32_text[::-1])])


if __name__ == '__main__':
    pass