import subprocess
import os
import pytest

def test_lcg_zero_c_parameter():
    """Verify that LCG parameters are correctly recognized even if 'c' is 0."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # a=1, c=0, m=100. If last_value=42, next should be 42.
    result = subprocess.run(
        ["python3", "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "42", "--a", "1", "--c", "0", "--m", "100"],
        capture_output=True,
        text=True,
        env=env
    )

    # If it tries to crack, it will fail because we only gave 1 value
    assert "Predicting next value with known parameters: 42" in result.stdout
    assert "Attempting to crack LCG parameters..." not in result.stdout

def test_lcg_dos_limit():
    """Verify that crack_lcg handles a large number of states gracefully by limiting processing."""
    # We can't easily test memory exhaustion, but we can check if it works with many states
    # and maybe verify that it only uses the first 100 if we could spy on it.
    # For now, just ensure it doesn't crash.
    from rng_decipherer.lcg import crack_lcg

    a = 1103515245
    c = 12345
    m = 2**31
    states = [42]
    for _ in range(200):
        states.append((a * states[-1] + c) % m)

    # This should still work if it takes the first 100
    cracked_a, cracked_c, cracked_m = crack_lcg(states)
    assert cracked_a == a
    assert cracked_c == c
    assert cracked_m == m
