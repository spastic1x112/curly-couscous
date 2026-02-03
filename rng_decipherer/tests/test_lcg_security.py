import pytest
from rng_decipherer.lcg import LCGPredictor, crack_lcg
import subprocess
import os
import sys

def test_lcg_crack_dos_limit():
    """Verify that crack_lcg limits input to 100 states."""
    # We can't directly check the internal 'states' variable, but we can
    # provide a sequence that would result in a different 'm' if
    # more than 100 states are used.

    # First 100 states: m = 2**31
    # 101st state: breaks the pattern
    a = 1103515245
    c = 12345
    m = 2**31
    states = [42]
    for _ in range(99):
        states.append((a * states[-1] + c) % m)

    # 100 states so far. If we add one more that doesn't follow the pattern:
    states.append(123456789) # 101st state

    # crack_lcg should only use the first 100 and succeed
    cracked_a, cracked_c, cracked_m = crack_lcg(states)
    assert cracked_a == a
    assert cracked_c == c
    assert cracked_m == m

def test_lcg_crack_invalid_m():
    """Verify that crack_lcg raises ValueError if m <= 1."""
    # Constant sequence: states = [7, 7, 7, 7, 7, 7]
    # diffs = [0, 0, 0, 0, 0]
    # multiples = [0, 0, 0]
    # m = gcd(0, 0, 0) = 0
    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg([7, 7, 7, 7, 7, 7])

def test_cli_lcg_zero_params():
    """Verify that the CLI correctly handles LCG parameters that are 0."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # a=0, c=5, m=10. Next value after 7 should be (0*7 + 5) % 10 = 5.
    result = subprocess.run(
        [sys.executable, "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "7", "--a", "0", "--c", "5", "--m", "10"],
        capture_output=True,
        text=True,
        env=env
    )

    assert "Predicting next value with known parameters: 5" in result.stdout

def test_lcg_mod_inverse_exception():
    """Verify that modInverse raises ValueError, not Exception."""
    from rng_decipherer.lcg import modInverse
    with pytest.raises(ValueError, match="modular inverse does not exist"):
        modInverse(2, 10) # 2 and 10 are not coprime, so no inverse

if __name__ == "__main__":
    pytest.main([__file__])
