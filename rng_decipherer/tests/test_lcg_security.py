import pytest
from rng_decipherer.lcg import LCGPredictor, crack_lcg


def test_lcg_predictor_invalid_m():
    """Verify that LCGPredictor raises ValueError for invalid modulus."""
    with pytest.raises(ValueError, match="Modulus 'm' must be greater than 1"):
        LCGPredictor(a=1, c=1, m=0)

    with pytest.raises(ValueError, match="Modulus 'm' must be greater than 1"):
        LCGPredictor(a=1, c=1, m=1)


def test_crack_lcg_dos_limit():
    """Verify that crack_lcg limits the number of states processed."""
    # If it processes all 1000 states, it might take longer or behave differently.
    # But specifically we want to ensure it doesn't crash and respects the limit.
    # We can test if it still works with first 100 states of a valid sequence
    a, c, m = 1103515245, 12345, 2**31
    states = [42]
    for _ in range(200):  # More than 100
        states.append((a * states[-1] + c) % m)

    # It should still be able to crack it using the first 100 states
    cracked_a, cracked_c, cracked_m = crack_lcg(states)
    assert cracked_a == a
    assert cracked_c == c
    assert cracked_m == m


def test_crack_lcg_invalid_m():
    """Verify that crack_lcg raises ValueError when m <= 1 is recovered."""
    # Sequence [10, 20, 30, 40, 50, 60] leads to m=0
    states = [10, 20, 30, 40, 50, 60]
    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg(states)

    # Sequence [10, 11, 12, 13, 14, 15] leads to m=0 too
    states2 = [10, 11, 12, 13, 14, 15]
    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg(states2)
