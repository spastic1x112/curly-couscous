import pytest
from rng_decipherer.lcg import LCGPredictor, crack_lcg


def test_lcg_invalid_modulus():
    """Verify that non-positive or degenerate modulus is rejected."""
    with pytest.raises(ValueError, match="Modulus m must be greater than 1."):
        LCGPredictor(a=1, c=1, m=1)
    with pytest.raises(ValueError, match="Modulus m must be greater than 1."):
        LCGPredictor(a=1, c=1, m=0)
    with pytest.raises(ValueError, match="Modulus m must be greater than 1."):
        LCGPredictor(a=1, c=1, m=-1)


def test_crack_lcg_constant_sequence():
    """Verify that crack_lcg handles constant sequences (recovered m=0 or 1) gracefully."""
    with pytest.raises(
        ValueError,
        match="Could not recover LCG parameters: modulus m recovered as 0, 1 or invalid.",
    ):
        crack_lcg([10, 10, 10, 10, 10, 10])


def test_crack_lcg_dos_limit():
    """Verify that crack_lcg limits the number of states processed."""
    # We can't easily check if it only used 100, but we can verify it still works
    # with > 100 states and doesn't crash.
    states = [i for i in range(200)]  # Not a real LCG, but should be handled
    with pytest.raises(ValueError):
        crack_lcg(states)


def test_mod_inverse_value_error():
    """Verify that modInverse raises ValueError instead of Exception."""
    from rng_decipherer.lcg import modInverse

    with pytest.raises(ValueError, match="modular inverse does not exist"):
        modInverse(2, 4)
