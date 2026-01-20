import pytest
import os
import tempfile
from rng_decipherer.mt19937 import MT19937Predictor


def test_mt19937_input_validation():
    predictor = MT19937Predictor()

    # Valid input
    predictor.feed(0)
    predictor.feed(0xFFFFFFFF)

    # Invalid input: too large
    with pytest.raises(
        ValueError, match="MT19937 values must be 32-bit unsigned integers"
    ):
        predictor.feed(0x100000000)

    # Invalid input: negative
    with pytest.raises(
        ValueError, match="MT19937 values must be 32-bit unsigned integers"
    ):
        predictor.feed(-1)

    # Invalid input: not an int
    with pytest.raises(
        ValueError, match="MT19937 values must be 32-bit unsigned integers"
    ):
        predictor.feed("123")


def test_cli_mt19937_large_file_limit(capsys):
    from rng_decipherer.cli import main
    import sys
    from unittest.mock import patch

    # Create a large file with more than 624 values
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        for i in range(1000):
            f.write(f"{i}\n")
        large_file_path = f.name

    try:
        # We need to mock sys.argv
        test_args = ["rng-decipherer", "mt19937", "--file", large_file_path]
        with patch.object(sys, "argv", test_args):
            # We also want to avoid actually running the predictor logic if we just want to check file reading,
            # but since we want to verify it works, we let it run.
            # We expect it to succeed and print "Reconstructed state successfully."
            # because 1000 > 624.
            # Run main
            main()

            captured = capsys.readouterr()
            assert "Reconstructed state successfully." in captured.out
            # The next predicted values will be based on the first 624 values (0 to 623)
    finally:
        os.remove(large_file_path)


def test_cli_mt19937_invalid_file_content(capsys):
    from rng_decipherer.cli import main
    import sys
    from unittest.mock import patch

    # Create a file with invalid content
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("123\nabc\n456\n")
        invalid_file_path = f.name

    try:
        test_args = ["rng-decipherer", "mt19937", "--file", invalid_file_path]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit) as e:
                main()
            assert e.value.code == 1

            captured = capsys.readouterr()
            assert "Error: Invalid integer in file: abc" in captured.out
    finally:
        os.remove(invalid_file_path)
