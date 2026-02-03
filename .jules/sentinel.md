## 2025-05-14 - MT19937 State Reconstruction Validation
**Vulnerability:** Memory-exhaustion DoS and potential OverflowError in random.setstate().
**Learning:** Python's random.setstate() for MT19937 accepts integers up to the size of C's unsigned long (64-bit on many systems), but the algorithm expects 32-bit values. Providing values outside this range can lead to incorrect behavior or OverflowError. Additionally, reading unlimited input from files to collect state values can lead to DoS.
**Prevention:** Strictly validate that input values for MT19937 are 32-bit unsigned integers (0 to 2^32-1) and limit the number of values read from external files to the required amount (624 for MT19937).

## 2025-05-15 - Information Leakage and DoS in CLI File Reading
**Vulnerability:** CLI tool leaked sensitive file content in error messages and was vulnerable to memory-exhaustion DoS via extremely long lines in input files.
**Learning:** Default Python exceptions (like `ValueError` from `int()`) often echo the invalid input, which can be sensitive if the input comes from a file. Additionally, `for line in f` can exhaust memory if a file has no newlines.
**Prevention:** Use `raise ... from None` to suppress exception context when re-raising, and use `f.readline(limit)` to bound memory usage when reading potentially untrusted files. Wrap the CLI entry point in a generic try-except to prevent stack trace leakage.

## 2025-05-16 - Algorithmic Complexity DoS and Param Validation in LCG Cracking
**Vulnerability:** Denial-of-Service via unbounded input states and logic bypass due to truthiness checks on numeric parameters.
**Learning:** Functions that perform iterative math (like GCD on large lists) must bound their input size to prevent CPU exhaustion. Additionally, using `if value:` for numeric parameters can lead to unintended logic branches if `0` is a valid input.
**Prevention:** Explicitly slice input lists for mathematical routines to a safe maximum (e.g., `states[:100]`). Always use `is not None` when checking if optional numeric arguments were provided.
