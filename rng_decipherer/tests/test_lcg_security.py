import pytest
import time
from rng_decipherer.lcg import crack_lcg, LCGPredictor

def test_lcg_dos_prevention():
    """Verify that crack_lcg limits input processing to prevent DoS."""
    # 1,000,000 states that would result in m=0 (degenerate case)
    # Without limit, it would process all 1,000,000.
    # With limit, it should only process 100.
    states = [1] * 1000000

    start_time = time.time()
    with pytest.raises(ValueError, match="Could not recover valid LCG parameters"):
        crack_lcg(states)
    duration = time.time() - start_time

    # Processing 1,000,000 integers should take significantly longer than 100.
    # 0.1 seconds is a very generous upper bound for processing 100 states.
    assert duration < 0.1, f"crack_lcg took too long: {duration:.4f}s"

def test_lcg_predictor_invalid_m():
    """Verify that LCGPredictor rejects m <= 1."""
    with pytest.raises(ValueError, match="Modulus 'm' must be greater than 1"):
        LCGPredictor(a=1, c=1, m=0)

    with pytest.raises(ValueError, match="Modulus 'm' must be greater than 1"):
        LCGPredictor(a=1, c=1, m=1)

def test_crack_lcg_invalid_m():
    """Verify that crack_lcg rejects cases resulting in m <= 1."""
    # Identical states result in m=0
    states = [123] * 10
    with pytest.raises(ValueError, match="Could not recover valid LCG parameters"):
        crack_lcg(states)

    # States that might result in m=1 (unlikely for real LCG but theoretically possible in the crack algorithm)
    # If m=1 is recovered, it should be rejected.
    # To force m=1, we can find states that make all multiples have GCD of 1.
    # Actually, any states that result in GCD 1 will work.
    states = [1, 2, 4, 8, 16, 33] # randomish enough to probably have gcd 1
    # Let's check:
    # diffs = [1, 2, 4, 8, 17]
    # multiples = [abs(4*1 - 2**2)=0, abs(8*2 - 4**2)=0, abs(17*4 - 8**2)=68-64=4]
    # GCD(0, 0, 4) = 4.

    states = [1, 2, 4, 7, 12, 21]
    # diffs = [1, 2, 3, 5, 9]
    # multiples = [abs(3*1 - 2**2)=1, ...] -> GCD will be 1
    with pytest.raises(ValueError, match="Could not recover valid LCG parameters"):
        crack_lcg(states)
