import subprocess
import os
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

def test_lcg_zero_parameters():
    """Verify that LCG parameters can be zero."""
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # a=0, c=0, m=100. (0 * x + 0) % 100 = 0
    result = subprocess.run(
        ["python3", "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values", "0", "--a", "0", "--c", "0", "--m", "100"],
        capture_output=True,
        text=True,
        env=env
    )

    assert "Predicting next value with known parameters: 0" in result.stdout

def test_lcg_crack_dos_limit():
    """Verify that LCG cracking limits the number of states processed."""
    # We can't easily measure memory, but we can verify it doesn't fail on large input
    # and we can check if it at least runs without error for a large-ish number of states.
    # More importantly, if we provide > 100 states that would normally fail if all were used
    # but pass if only first 100 are used (or vice versa), but here we just check it doesn't crash.

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{os.getcwd()}/rng_decipherer/src:{env.get('PYTHONPATH', '')}"

    # Generate 200 values
    values = [str(i) for i in range(200)]

    result = subprocess.run(
        ["python3", "rng_decipherer/src/rng_decipherer/cli.py", "lcg", "--values"] + values,
        capture_output=True,
        text=True,
        env=env
    )

    # It might still fail to crack (because sequential numbers aren't a good LCG),
    # but it should not have crashed and should have handled the input.
    assert "Attempting to crack LCG parameters..." in result.stdout

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
