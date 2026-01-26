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

def test_lcg_dos():
    """Verify that crack_lcg limits the number of states to prevent DoS."""
    from rng_decipherer.lcg import crack_lcg
    import time

    large_states = list(range(1000000))
    start_time = time.time()
    try:
        crack_lcg(large_states)
    except ValueError:
        pass
    end_time = time.time()

    # Should be very fast
    assert end_time - start_time < 0.1

def test_lcg_invalid_modulus():
    """Verify that crack_lcg and LCGPredictor handle m <= 1."""
    from rng_decipherer.lcg import crack_lcg, LCGPredictor
    import pytest

    # Sequence that results in m=0
    with pytest.raises(ValueError, match="Could not recover a valid modulus m > 1"):
        crack_lcg([1, 1, 1, 1, 1, 1])

    # Predictor with invalid m
    predictor = LCGPredictor(a=1, c=1, m=1)
    predictor.feed(0)
    with pytest.raises(ValueError, match="Modulus m must be greater than 1"):
        predictor.predict_next()

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
