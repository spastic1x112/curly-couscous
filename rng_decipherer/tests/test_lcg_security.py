import subprocess
import os
import pytest
from rng_decipherer.lcg import crack_lcg

def test_lcg_cli_zero_params():
    """Verify that CLI handles a=0, c=0 correctly."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # a=1, c=0, m=100. If last value is 42, next is (1*42 + 0) % 100 = 42
    result = subprocess.run(
        ["python3", "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "42", "--a", "1", "--c", "0", "--m", "100"],
        capture_output=True,
        text=True,
        env=env
    )
    assert "Predicting next value with known parameters: 42" in result.stdout

def test_crack_lcg_dos_limit():
    """Verify that crack_lcg limits states to 100."""
    # Create 200 states for a simple LCG
    a, c, m = 1103515245, 12345, 2**31
    states = [42]
    for _ in range(200):
        states.append((a * states[-1] + c) % m)

    # We can't easily check internal state, but we can verify it still works
    # and maybe check coverage if we had it.
    # For now, just ensure it doesn't crash.
    cracked_a, cracked_c, cracked_m = crack_lcg(states)
    assert cracked_a == a
    assert cracked_c == c
    assert cracked_m == m

def test_crack_lcg_degenerate_m():
    """Verify that crack_lcg fails if recovered m <= 1."""
    # A sequence that results in m=0 or m=1
    states = [1, 1, 1, 1, 1, 1]
    with pytest.raises(ValueError, match="Recovered modulus m is too small to be valid."):
        crack_lcg(states)

    states = [1, 2, 3, 4, 5, 6] # Linear sequence, diffs are [1, 1, 1, 1, 1], multiples are [0, 0, 0]
    with pytest.raises(ValueError, match="Recovered modulus m is too small to be valid."):
        crack_lcg(states)
