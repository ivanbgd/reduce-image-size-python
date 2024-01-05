from enum import IntEnum

QUALITY = 75
"""JPEG quality default value"""


class Size(IntEnum):
    """ A minimum file size for which to perform file size reduction.

        - DEFAULT = 0
        - S = 100 kB
        - M = 500 kB
        - L = 1 MB
    """
    DEFAULT = 0
    S = 102400
    M = 512000
    L = 1048576
