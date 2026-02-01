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
            [sys.executable, "rng_decipherer/src/rng_decipherer/cli.py", "mt19937", "--file", file_path],
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

def test_lcg_crack_dos_limit():
    """Verify that crack_lcg limits the number of states it processes."""
    from rng_decipherer.lcg import crack_lcg
    # If it doesn't limit, this might be slow or consume more memory
    # but more importantly, we want to check it raises a ValueError if we can
    # identify it's too much, OR it just uses the first 100.
    # The requirement is to limit to 100.
    states = list(range(1000))
    # If it limits to 100, and they are linear [0, 1, 2...99], m will be 0.
    # We should ensure it doesn't try to process all 1000.
    with pytest.raises(ValueError):
        crack_lcg(states)

def test_lcg_invalid_m_zero():
    """Verify that crack_lcg handles sequences that would result in m=0."""
    from rng_decipherer.lcg import crack_lcg
    states = [1, 2, 3, 4, 5, 6] # Linear sequence, gcd of multiples will be 0
    with pytest.raises(ValueError, match="Recovered modulus m must be greater than 1"):
        crack_lcg(states)

def test_lcg_invalid_m_one():
    """Verify that crack_lcg handles sequences that would result in m=1."""
    from rng_decipherer.lcg import crack_lcg
    states = [0, 0, 0, 0, 0, 0]
    with pytest.raises(ValueError, match="Recovered modulus m must be greater than 1"):
        crack_lcg(states)

def test_cli_lcg_zero_params():
    """Verify that the CLI correctly handles 0 as a valid LCG parameter."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # a=0, c=1, m=10, last_value=5 -> (0*5 + 1) % 10 = 1
    result = subprocess.run(
        [sys.executable, "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "5", "--a", "0", "--c", "1", "--m", "10"],
        capture_output=True,
        text=True,
        env=env
    )
    assert "Predicting next value with known parameters: 1" in result.stdout

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
            [sys.executable, "rng_decipherer/src/rng_decipherer/cli.py", "mt19937", "--file", file_path],
            capture_output=True,
            text=True,
            env=env
        )

        # It should fail because "AAAA..." is not an int, but it should fail gracefully
        assert "Error: Invalid integer value found in file." in result.stdout or "Error: Invalid integer value found in file." in result.stderr

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
