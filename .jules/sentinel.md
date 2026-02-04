## 2025-05-14 - MT19937 State Reconstruction Validation
**Vulnerability:** Memory-exhaustion DoS and potential OverflowError in random.setstate().
**Learning:** Python's random.setstate() for MT19937 accepts integers up to the size of C's unsigned long (64-bit on many systems), but the algorithm expects 32-bit values. Providing values outside this range can lead to incorrect behavior or OverflowError. Additionally, reading unlimited input from files to collect state values can lead to DoS.
**Prevention:** Strictly validate that input values for MT19937 are 32-bit unsigned integers (0 to 2^32-1) and limit the number of values read from external files to the required amount (624 for MT19937).

## 2025-05-15 - Information Leakage and DoS in CLI File Reading
**Vulnerability:** CLI tool leaked sensitive file content in error messages and was vulnerable to memory-exhaustion DoS via extremely long lines in input files.
**Learning:** Default Python exceptions (like `ValueError` from `int()`) often echo the invalid input, which can be sensitive if the input comes from a file. Additionally, `for line in f` can exhaust memory if a file has no newlines.
**Prevention:** Use `raise ... from None` to suppress exception context when re-raising, and use `f.readline(limit)` to bound memory usage when reading potentially untrusted files. Wrap the CLI entry point in a generic try-except to prevent stack trace leakage.

## 2025-05-16 - LCG Cracking Denial-of-Service and Parameter Validation
**Vulnerability:** Resource exhaustion (DoS) via unlimited state input and logic errors in parameter validation.
**Learning:** GCD and large-number arithmetic in LCG cracking can be computationally expensive if the number of input states is unbounded. Additionally, using truthiness checks (e.g., `if args.c`) for numeric parameters can lead to incorrect program flow when `0` is a valid input, potentially bypassing intended security or logic paths.
**Prevention:** Hard-limit the number of observed states used for PRNG cracking (e.g., limit to 100 for LCG). Always use `is not None` for numeric parameter validation to correctly handle zero-values. Validate that recovered mathematical parameters (like modulus 'm') meet minimum security/sanity requirements (m > 1).
