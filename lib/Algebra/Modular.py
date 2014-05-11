__author__ = 'nessvm'

"""This module contains al algebraic functions that wil be used for
the voting system implementation.
"""


def mod_inv(z, n):
    """Returns the inverse of the number z modulo n"""

    for i in range(n):
        if (z * i) % n == 1:
            return i

    return None