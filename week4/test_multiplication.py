"""
Randomized cross-check of multiply_classic and multiply_karatsuba against
Python's built-in * operator.

For each length in {1, 2, 4, 8, 16}, generate several random same-length
digit pairs, pad them to a matching power-of-two length, run both
algorithms, strip the padding zeros, and compare to plain integer
multiplication. Also checks the all-9s case explicitly, since it forces a
carry out of every single digit position.
"""

import random

from multiplication import (
    from_int,
    to_int,
    pad_to_power_of_two,
    strip_leading_zeros,
    multiply_classic,
    multiply_karatsuba,
    random_digits,
)

LENGTHS = [1, 2, 4, 8, 16]
TRIALS_PER_LENGTH = 200


def check(x, y, label):
    """Multiply x and y with both algorithms and compare to x * y."""
    xp, yp = pad_to_power_of_two(x, y)
    expected = to_int(x) * to_int(y)

    classic = to_int(strip_leading_zeros(multiply_classic(xp, yp)))
    karatsuba = to_int(strip_leading_zeros(multiply_karatsuba(xp, yp)))

    ok = (classic == expected) and (karatsuba == expected)
    status = "OK" if ok else "MISMATCH"
    print(f"[{status}] {label}: {to_int(x)} x {to_int(y)} "
          f"-> expected={expected} classic={classic} karatsuba={karatsuba}")
    return ok


def main():
    rng = random.Random(363)
    all_ok = True

    # All-9s case: exercises a carry out of every digit position.
    nines = [9] * 8
    all_ok &= check(nines, nines, "all-9s (len 8)")

    for n in LENGTHS:
        for trial in range(TRIALS_PER_LENGTH):
            x = random_digits(n, rng)
            y = random_digits(n, rng)
            all_ok &= check(x, y, f"len {n}, trial {trial}")

    print()
    print("ALL TESTS PASSED" if all_ok else "SOME TESTS FAILED")


if __name__ == "__main__":
    main()