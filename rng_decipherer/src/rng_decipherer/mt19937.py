def unBitshiftRight(y, shift):
    x = y
    for _ in range(32 // shift):
        x = y ^ (x >> shift)
    return x

def unBitshiftLeftMask(y, shift, mask):
    x = y
    for _ in range(32 // shift):
        x = y ^ ((x << shift) & mask)
    return x

def untemper(y):
    """Reverses the tempering steps of MT19937."""
    y = unBitshiftRight(y, 18)
    y = unBitshiftLeftMask(y, 15, 0xefc60000)
    y = unBitshiftLeftMask(y, 7, 0x9d2c5680)
    y = unBitshiftRight(y, 11)
    return y

class MT19937Predictor:
    def __init__(self):
        self.state = []

    def feed(self, value):
        """Feed a 32-bit output value to reconstruct the state."""
        if not isinstance(value, int) or not (0 <= value <= 0xFFFFFFFF):
            raise ValueError(f"Value {value} is not a valid 32-bit unsigned integer.")
        if len(self.state) < 624:
            self.state.append(untemper(value))

    def get_random_instance(self):
        """Returns a python random.Random instance with the reconstructed state."""
        import random
        if len(self.state) != 624:
            raise ValueError(f"Need exactly 624 values to reconstruct state, got {len(self.state)}.")

        # Python's random.getstate() returns (3, state, None)
        # where state is a tuple of 624 integers and the index 624.
        state_tuple = (3, tuple(self.state + [624]), None)
        r = random.Random()
        r.setstate(state_tuple)
        return r
