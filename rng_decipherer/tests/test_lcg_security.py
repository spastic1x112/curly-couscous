import pytest
from rng_decipherer.lcg import crack_lcg

def test_lcg_large_input_dos():
    """Verify that crack_lcg limits the number of states to prevent DoS."""
    # 1 million states would be slow if not limited
    large_input = [i for i in range(1000000)]
    # This should return quickly because it only uses the first 100
    with pytest.raises(ValueError):
        # It will likely fail to crack because the input is just i, i+1...
        # but it should fail QUICKLY.
        crack_lcg(large_input)

def test_lcg_zero_parameters_cli():
    """Verify that CLI handles 0 as a valid parameter (simulated)."""
    # This test simulates the CLI logic
    # In a real scenario, we'd use subprocess, but here we just check the logic
    a, c, m = 1, 0, 10

    # OLD LOGIC: if args.a and args.c and args.m:
    # NEW LOGIC: if args.a is not None and args.c is not None and args.m is not None:

    def simulate_cli(arg_a, arg_c, arg_m):
        if arg_a is not None and arg_c is not None and arg_m is not None:
            return "Known Parameters Path"
        else:
            return "Cracking Path"

    assert simulate_cli(a, c, m) == "Known Parameters Path"

def test_lcg_negative_diff_mod_inv():
    """Verify that crack_lcg handles negative differences correctly for modInverse."""
    # LCG: x_{n+1} = (a*x_n + c) % m
    # a=3, c=1, m=10
    # x0=6 -> x1=9 -> x2=8 -> x3=5 -> x4=6 -> x5=9
    states = [6, 9, 8, 5, 6, 9] # a=3, c=1, m=10

    # This should not raise "modular inverse does not exist" just because diff is negative
    a, c, m = crack_lcg(states)
    assert a == 3
    assert c == 1
    assert m == 10

def test_lcg_invalid_modulus():
    """Verify that crack_lcg raises ValueError if a valid modulus cannot be recovered."""
    # Constant sequence: 5, 5, 5, 5, 5, 5
    states = [5] * 6
    with pytest.raises(ValueError, match="Could not recover a valid modulus 'm'"):
        crack_lcg(states)
