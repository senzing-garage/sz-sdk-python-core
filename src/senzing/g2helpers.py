"""
TODO: g2helpers.py
"""


def as_normalized_int(candidate_value: any) -> int:
    # type: (str) -> int
    """
    Internal processing function
    This converts many types of values to an integer
    """

    if candidate_value is None:  # handle null string
        return 0
    if isinstance(candidate_value, str):  # if string is unicode, transcode to utf-8 str
        return int(candidate_value.encode("utf-8"))
    if isinstance(
        candidate_value, bytearray
    ):  # if input is bytearray, assumt utf-8 and convert to str
        return int(candidate_value)
    if isinstance(candidate_value, bytes):
        return int(candidate_value)
    # input is already an int
    return candidate_value


def as_normalized_string(candidate_value: any) -> str:
    """Internal processing function"""

    if candidate_value is None:  # handle null string
        return b""
    if isinstance(candidate_value, str):  # if string is unicode, transcode to utf-8 str
        return candidate_value.encode("utf-8")
    if isinstance(
        candidate_value, bytearray
    ):  # if input is bytearray, assumt utf-8 and convert to str
        return candidate_value.decode().encode("utf-8")
    if isinstance(candidate_value, bytes):
        return str(candidate_value).encode("utf-8")
    # input is already a str
    return candidate_value
