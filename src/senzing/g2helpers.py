"""
TODO: g2helpers.py
"""


def as_normalized_int(candidate_value: any) -> int:
    # type: (str) -> int
    """ Internal processing function """
    """ This converts many types of values to an integer """

    # handle null string
    if candidate_value is None:
        return 0
    # if string is unicode, transcode to utf-8 str
    if type(candidate_value) == str:
        return int(candidate_value.encode('utf-8'))
    # if input is bytearray, assumt utf-8 and convert to str
    elif type(candidate_value) == bytearray:
        return int(candidate_value)
    elif type(candidate_value) == bytes:
        return int(candidate_value)
    # input is already an int
    return candidate_value


def as_normalized_string(candidate_value: any) -> str:
    """ Internal processing function """
    # handle null string
    if candidate_value is None:
        return b''
    # if string is unicode, transcode to utf-8 str
    if type(candidate_value) == str:
        return candidate_value.encode('utf-8')
    # if input is bytearray, assumt utf-8 and convert to str
    elif type(candidate_value) == bytearray:
        return candidate_value.decode().encode('utf-8')
    elif type(candidate_value) == bytes:
        return str(candidate_value).encode('utf-8')
    # input is already a str
    return candidate_value
