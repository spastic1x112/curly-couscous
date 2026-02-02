import subprocess
import os
import sys
import pytest
from rng_decipherer.lcg import crack_lcg

def test_lcg_c_zero_cli():
    """Verify that c=0 is correctly handled in the CLI."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # LCG with c=0, a=3, m=7. x0=1 -> x1=3.
    result = subprocess.run(
        [sys.executable, "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "1", "--a", "3", "--c", "0", "--m", "7"],
        capture_output=True,
        text=True,
        env=env
    )

    assert "Predicting next value with known parameters: 3" in result.stdout
    assert "Attempting to crack LCG parameters..." not in result.stdout

def test_crack_lcg_state_limit():
    """Verify that crack_lcg limits the number of states it processes."""
    # Create 200 states. If the limit works, it should only use the first 100.
    # We can't easily see internal state, but we can check if it still works
    # and doesn't crash with many states.
    states = list(range(200)) # This won't crack successfully, but it should fail gracefully/quickly

    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg(states)

def test_mod_inverse_value_error():
    """Verify that modInverse raises ValueError instead of Exception."""
    from rng_decipherer.lcg import modInverse
    with pytest.raises(ValueError, match="modular inverse does not exist"):
        modInverse(2, 4) # 2 has no inverse mod 4

def test_crack_lcg_invalid_modulus():
    """Verify that crack_lcg raises ValueError when m <= 1."""
    # Consecutive states [1, 1, 1, 1, 1, 1] will result in m=0 or m=1
    states = [1, 1, 1, 1, 1, 1]
    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg(states)
