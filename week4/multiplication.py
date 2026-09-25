"""
multiplication.py -- COMP 363, Week 04

Divide-and-conquer multiplication of large numbers, in pure Python.

REPRESENTATION
    A number is a list of decimal digits, most significant digit first:

        1234  ->  [1, 2, 3, 4]        11  ->  [1, 1]        7  ->  [7]

    The two principal functions, multiply_classic(x, y) and
    multiply_karatsuba(x, y), expect x and y to have the same length, and
    that length must be a power of 2 (1, 2, 4, 8, ...). Use
    pad_to_power_of_two(x, y) to get there from arbitrary lists. Each
    principal function returns a list of exactly 2*n digits, where n is the
    length of the inputs (leading zeros included).

ALLOWED ARITHMETIC
    Everything below is built from just three operations on single digits:
        * multiplying one digit by one digit  (multiply_digits, and the
          0/1 "selector" multiplication in scale_by_bit)
        * adding digits, with carry           (add_digits)
        * subtracting digits, with borrow     (subtract_digits)
    Python's built-in big integers are NEVER used to compute a product.
    (to_int / from_int exist only so you can check answers and print
    results; the multiplication functions never call them.)

THE TWO RECURSIONS
    Split each n-digit number into halves, x = A|B and y = C|D, so that
        x = A * 10^(n/2) + B        y = C * 10^(n/2) + D

    Classic (4 recursive products of size n/2):
        xy = AC * 10^n + (BC + AD) * 10^(n/2) + BD

    Karatsuba (3 recursive products of size n/2):
        xy = AC * 10^n + ((A+B)(C+D) - AC - BD) * 10^(n/2) + BD
"""

# ---------------------------------------------------------------------------
# Instrumentation: how many single-digit multiplications have been performed.
# Kept in a one-element list so the helper can update it without "global".
# Reset it with reset_digit_mult_count() before each experiment.
# ---------------------------------------------------------------------------
DIGIT_MULT_COUNT = [0]
import os
import random



def reset_digit_mult_count():
    """Set the single-digit multiplication counter back to zero."""
    DIGIT_MULT_COUNT[0] = 0


def get_digit_mult_count():
    """Return the number of single-digit multiplications since the last reset."""
    result = DIGIT_MULT_COUNT[0]
    return result


# ---------------------------------------------------------------------------
# Auxiliary functions shared by both algorithms
# ---------------------------------------------------------------------------

def multiply_digits(p, q):
    """
    Multiply two single digits p and q (each 0..9).

    The product is at most 81, so it always fits in two digits. It is
    returned as [tens, ones] -- for example 7 x 8 = 56 -> [5, 6], and
    2 x 3 = 6 -> [0, 6].
    """
    DIGIT_MULT_COUNT[0] += 1
    product = p * q                 # the one true multiplication in this file
    tens = 0
    while product >= 10:            # peel off tens by repeated subtraction
        product = product - 10
        tens = tens + 1
    result = [tens, product]
    return result


def scale_by_bit(x, bit):
    """
    Multiply every digit of x by bit, where bit is 0 or 1.

    This is a single-digit multiplication per position: it either keeps x
    unchanged (bit = 1) or replaces it with all zeros (bit = 0). Karatsuba
    uses it to handle the carry out of (A+B) and (C+D); see
    multiply_karatsuba.
    """
    result = [bit * digit for digit in x]
    return result


def next_power_of_two(n):
    """Return the smallest power of 2 that is >= n (for n >= 1)."""
    power = 1
    while power < n:
        power = power * 2
    return power


def pad_left(x, n):
    """
    Return a copy of x, left-padded with zeros to length exactly n.

    If x is already longer than n, its extra leading digits are removed --
    which is only correct when those digits are all zeros. Callers rely on
    this to trim carries that turned out to be 0.
    """
    length = len(x)
    if length <= n:
        result = [0] * (n - length) + x
    else:
        result = x[length - n:]
    return result


def pad_to_power_of_two(x, y):
    """
    Left-pad x and y with zeros to a common length that is a power of 2.

    Returns a pair (x_padded, y_padded) ready for the principal functions.
    Example: [1, 2, 3] and [4, 5, 6, 7, 8] both become length 8.
    """
    n = next_power_of_two(max(len(x), len(y)))
    result = (pad_left(x, n), pad_left(y, n))
    return result


def split_in_half(x):
    """
    Split x (even length n) into its high half and low half, (A, B), so
    that x = A * 10^(n/2) + B.  Example: [1, 2, 3, 4] -> ([1, 2], [3, 4]).
    """
    half = len(x) // 2
    result = (x[:half], x[half:])
    return result


def shift(x, k):
    """
    Multiply x by 10^k by appending k zeros on the right.
    Example: shift([1, 2], 3) -> [1, 2, 0, 0, 0].
    """
    result = x + [0] * k
    return result


def add_digits(x, y):
    """
    Add two digit lists, digit by digit, right to left, carrying as needed.

    The shorter list is left-padded with zeros first. The answer has one
    more digit than the longer input, to hold a possible final carry (which
    is often 0). Example: [9, 9] + [1] -> [1, 0, 0].
    """
    n = max(len(x), len(y))
    xs = pad_left(x, n)
    ys = pad_left(y, n)
    result = [0] * (n + 1)
    carry = 0
    for i in range(n - 1, -1, -1):          # least significant digit first
        column = xs[i] + ys[i] + carry      # at most 9 + 9 + 1 = 19
        if column >= 10:
            result[i + 1] = column - 10
            carry = 1
        else:
            result[i + 1] = column
            carry = 0
    result[0] = carry
    return result


def subtract_digits(x, y):
    """
    Compute x - y, digit by digit, right to left, borrowing as needed.

    Requires x >= y as numbers. The shorter list is left-padded with zeros;
    the answer has the same length as the longer input.
    Example: [1, 0, 0] - [9] -> [0, 9, 1].
    """
    n = max(len(x), len(y))
    xs = pad_left(x, n)
    ys = pad_left(y, n)
    result = [0] * n
    borrow = 0
    for i in range(n - 1, -1, -1):          # least significant digit first
        column = xs[i] - ys[i] - borrow
        if column < 0:
            result[i] = column + 10
            borrow = 1
        else:
            result[i] = column
            borrow = 0
    return result


# ---------------------------------------------------------------------------
# Principal function 1: classic recursive multiplication
# ---------------------------------------------------------------------------

def multiply_classic(x, y):
    """
    Multiply x and y (equal length n, a power of 2) with four recursive
    # half-size products:

        xy = AC * 10^n + (BC + AD) * 10^(n/2) + BD

    Base case: n = 1, a single-digit multiplication.
    Returns a list of exactly 2n digits.
    """
    n = len(x)
    if n == 1:
        result = multiply_digits(x[0], y[0])
    else:
        half = n // 2
        A, B = split_in_half(x)
        C, D = split_in_half(y)

        AC = multiply_classic(A, C)             # each product has n digits
        BC = multiply_classic(B, C)
        AD = multiply_classic(A, D)
        BD = multiply_classic(B, D)

        middle = add_digits(BC, AD)             # n + 1 digits
        total = add_digits(shift(AC, n), shift(middle, half))
        total = add_digits(total, BD)
        result = pad_left(total, 2 * n)         # xy < 10^(2n): top carries are 0
    return result


# ---------------------------------------------------------------------------
# Principal function 2: Karatsuba multiplication
# ---------------------------------------------------------------------------    

def multiply_karatsuba(x, y):
    """
    Multiply x and y (equal length n, a power of 2) with THREE recursive
    half-size products:

        xy = AC * 10^n + ((A+B)(C+D) - AC - BD) * 10^(n/2) + BD

    Base case: n = 1, a single-digit multiplication.
    Returns a list of exactly 2n digits.

    A wrinkle: A+B can be an (n/2 + 1)-digit number, because of a carry out
    of its top digit. If we fed that straight into the recursion the
    subproblem would not shrink (at n = 2 it would never stop). So we keep
    the carry aside. Write W = 10^(n/2) and

        A + B = carry_x * W + lo_AB   (lo_AB: low n/2 digits; carry_x is 0 or 1)
        C + D = carry_y * W + lo_CD   (lo_CD: low n/2 digits; carry_y is 0 or 1)

    Then
        (A+B)(C+D) = carry_x*carry_y * W^2
                     + (carry_x*lo_CD + carry_y*lo_AB) * W
                     + lo_AB*lo_CD

    and only lo_AB*lo_CD is a real (half-size) recursive product; the rest is
    shifting, adding, and multiplying by the 0/1 carries (scale_by_bit).
    """
    n = len(x)
    if n == 1:
        result = multiply_digits(x[0], y[0])
    else:
        half = n // 2
        A, B = split_in_half(x)
        C, D = split_in_half(y)

        AC = multiply_karatsuba(A, C)           # recursive product 1
        BD = multiply_karatsuba(B, D)           # recursive product 2

        sum_AB = add_digits(A, B)               # half + 1 digits
        sum_CD = add_digits(C, D)
        carry_x, lo_AB = sum_AB[0], sum_AB[1:]   # split off the carry digit
        carry_y, lo_CD = sum_CD[0], sum_CD[1:]

        lo_product = multiply_karatsuba(lo_AB, lo_CD)   # recursive product 3

        # (A+B)(C+D) = carry_x*carry_y*W^2 + (carry_x*lo_CD + carry_y*lo_AB)*W
        #              + lo_AB*lo_CD,   where W = 10^half
        carry_carry = [carry_x * carry_y]       # 1 digit
        cross = add_digits(scale_by_bit(lo_CD, carry_x), scale_by_bit(lo_AB, carry_y))
        full = add_digits(shift(carry_carry, n), shift(cross, half))
        full = add_digits(full, lo_product)
        full = pad_left(full, n + 2)            # (A+B)(C+D) < 4 * 10^n

        # (A+B)(C+D) - AC - BD  =  BC + AD
        middle = subtract_digits(subtract_digits(full, AC), BD)

        total = add_digits(shift(AC, n), shift(middle, half))
        total = add_digits(total, BD)
        result = pad_left(total, 2 * n)
    return result


# ---------------------------------------------------------------------------
# Conveniences for testing and printing (NOT used by the multiplications)
# ---------------------------------------------------------------------------

def from_int(value):
    """Convert a non-negative Python int to a digit list. from_int(11) -> [1, 1]."""
    result = [int(ch) for ch in str(value)]
    return result


def to_int(x):
    """Convert a digit list to a Python int. to_int([0, 1, 2, 1]) -> 121."""
    result = int("".join(str(digit) for digit in x))
    return result


def strip_leading_zeros(x):
    """Drop leading zeros from x, keeping at least one digit."""
    start = 0
    while start < len(x) - 1 and x[start] == 0:
        start = start + 1
    result = x[start:]
    return result


def random_digits(n, rng):
    """
    Return a list of n random digits with a nonzero leading digit.
    rng is a random.Random instance, supplied by the caller so that this
    module needs no imports; e.g. random_digits(8, random.Random(363)).
    """
    result = [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(n - 1)]
    return result


# ---------------------------------------------------------------------------
# Demonstration: python3 multiplication.py
# ---------------------------------------------------------------------------

def main():
    """Run the 11 x 11 example and a small self-check of both algorithms."""
    x, y = [1, 1], [1, 1]
    print("classic  ([1,1],[1,1]) ->", multiply_classic(x, y))
    print("karatsuba([1,1],[1,1]) ->", multiply_karatsuba(x, y))

    x, y = pad_to_power_of_two(from_int(12), from_int(34))
    print("padded operands:", x, y)
    print("classic  ->", strip_leading_zeros(multiply_classic(x, y)))
    print("karatsuba->", strip_leading_zeros(multiply_karatsuba(x, y)))
    print("expected  ->", 123456 * 789)          # answer key only






if __name__ == "__main__":
    main()
