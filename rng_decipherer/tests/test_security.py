import subprocess
import os
import sys
import pytest

def test_mt19937_file_leak():
    """Verify that sensitive content in a file is not leaked in error messages."""
    secret_content = "SECRET_TOKEN_12345"
    file_path = "test_security_leak.txt"
    with open(file_path, "w") as f:
        f.write(secret_content + "\n")

    try:
        # Run the CLI tool
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

        # Need to point to the actual script or use python -m
        # Since it's in a package, we can use:
        result = subprocess.run(
            ["python3", "rng_decipherer/src/rng_decipherer/cli.py", "mt19937", "--file", file_path],
            capture_output=True,
            text=True,
            env=env
        )

        assert secret_content not in result.stdout
        assert secret_content not in result.stderr
        assert "Error: Invalid integer value found in file." in result.stdout or "Error: Invalid integer value found in file." in result.stderr

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def test_lcg_c_zero_param():
    """Verify that c=0 is correctly handled in LCG CLI."""
    # a=1103515245, c=0, m=2147483648, last_value=12345
    # next = (1103515245 * 12345 + 0) % 2147483648 = 1530391213
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    result = subprocess.run(
        [sys.executable, "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "12345", "--a", "1103515245", "--c", "0", "--m", "2147483648"],
        capture_output=True,
        text=True,
        env=env
    )
    assert "Predicting next value with known parameters: 1406920261" in result.stdout
    assert "Attempting to crack LCG parameters..." not in result.stdout

def test_lcg_dos_prevention():
    """Verify that LCG cracking limits the number of states to prevent DoS."""
    # Simple LCG: a=3, c=7, m=31, s0=1
    a, c, m = 3, 7, 31
    states = [1]
    for _ in range(110):
        states.append((a * states[-1] + c) % m)

    # states has 111 elements.
    # Append some junk that would break cracking if included (crack_lcg should only take first 100)
    bad_states = states + [999, 999, 999]

    from rng_decipherer.lcg import crack_lcg
    ca, cc, cm = crack_lcg(bad_states)
    assert (ca, cc, cm) == (a, c, m)

def test_lcg_invalid_m():
    """Verify that recovering an invalid modulus (m <= 1) raises ValueError."""
    from rng_decipherer.lcg import crack_lcg

    # Constant states lead to m=0
    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg([5, 5, 5, 5, 5, 5])

def test_mt19937_large_line_dos():
    """Verify that a very long line does not cause memory issues (basic check)."""
    # This is more of a smoke test to ensure it doesn't just hang/crash on a 2KB line
    large_content = "A" * 2048
    file_path = "test_security_dos.txt"
    with open(file_path, "w") as f:
        f.write(large_content + "\n")

    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

        result = subprocess.run(
            ["python3", "rng_decipherer/src/rng_decipherer/cli.py", "mt19937", "--file", file_path],
            capture_output=True,
            text=True,
            env=env
        )

        # It should fail because "AAAA..." is not an int, but it should fail gracefully
        assert "Error: Invalid integer value found in file." in result.stdout or "Error: Invalid integer value found in file." in result.stderr

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
