import math


def modInverse(a, m):
    """Calculates the modular multiplicative inverse of a modulo m."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    else:
        return x % m


def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y


class LCGPredictor:
    def __init__(self, a=None, c=None, m=None):
        self.a = a
        self.c = c
        self.m = m
        self.last_value = None

    def feed(self, value):
        self.last_value = value

    def predict_next(self):
        if (
            self.a is None
            or self.c is None
            or self.m is None
            or self.last_value is None
        ):
            raise ValueError("Parameters and last value must be known to predict next.")
        return (self.a * self.last_value + self.c) % self.m


def crack_lcg(states):
    """
    Cracks an LCG given enough consecutive states.
    Returns (a, c, m).
    """
    if len(states) < 6:
        raise ValueError("Need at least 6 states to crack LCG with unknown m.")

    # Limit states to prevent DoS via large inputs
    states = states[:100]

    # Recover m
    diffs = [states[i + 1] - states[i] for i in range(len(states) - 1)]
    multiples = [
        abs(diffs[i + 2] * diffs[i] - diffs[i + 1] ** 2) for i in range(len(diffs) - 2)
    ]

    m = multiples[0]
    for val in multiples[1:]:
        m = math.gcd(m, val)

    if m <= 1:
        raise ValueError("Could not recover a valid modulus 'm'.")

    # Recover a
    try:
        # states[1] - states[0] might be 0 mod m if m=1, but we checked m > 1.
        # However, it still might not have an inverse.
        a = (states[2] - states[1]) * modInverse(states[1] - states[0], m) % m
    except (ValueError, ArithmeticError, ZeroDivisionError, Exception) as e:
        # If inverse doesn't exist, we might need more states or a different approach.
        # We re-raise as ValueError to keep it generic for the caller.
        if isinstance(e, ValueError) and "modular inverse does not exist" in str(e):
            raise ValueError(
                "Could not recover 'a': modular inverse does not exist."
            ) from None
        raise ValueError("Could not recover 'a', parameter cracking failed.") from None

    # Recover c
    c = (states[1] - a * states[0]) % m

    return a, c, m
