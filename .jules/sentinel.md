## 2025-05-14 - MT19937 State Reconstruction Validation
**Vulnerability:** Memory-exhaustion DoS and potential OverflowError in random.setstate().
**Learning:** Python's random.setstate() for MT19937 accepts integers up to the size of C's unsigned long (64-bit on many systems), but the algorithm expects 32-bit values. Providing values outside this range can lead to incorrect behavior or OverflowError. Additionally, reading unlimited input from files to collect state values can lead to DoS.
**Prevention:** Strictly validate that input values for MT19937 are 32-bit unsigned integers (0 to 2^32-1) and limit the number of values read from external files to the required amount (624 for MT19937).

## 2025-05-15 - Information Leakage and DoS in CLI File Reading
**Vulnerability:** CLI tool leaked sensitive file content in error messages and was vulnerable to memory-exhaustion DoS via extremely long lines in input files.
**Learning:** Default Python exceptions (like `ValueError` from `int()`) often echo the invalid input, which can be sensitive if the input comes from a file. Additionally, `for line in f` can exhaust memory if a file has no newlines.
**Prevention:** Use `raise ... from None` to suppress exception context when re-raising, and use `f.readline(limit)` to bound memory usage when reading potentially untrusted files. Wrap the CLI entry point in a generic try-except to prevent stack trace leakage.

## 2025-05-16 - LCG Parameter Validation and DoS Prevention
**Vulnerability:** Denial of Service in LCG cracking and incorrect handling of 0 as a valid parameter.
**Learning:** Checking for the presence of numeric parameters using `if arg` fails when the value is 0. Additionally, mathematical algorithms like LCG parameter recovery can be vulnerable to DoS if the number of input states is not bounded, as they may perform expensive operations (like GCD) on large lists.
**Prevention:** Use `is not None` when validating optional numeric CLI arguments. Explicitly limit the number of input states for cracking algorithms to a reasonable maximum (e.g., 100 for LCG) and validate that recovered parameters (like the modulus) are within a valid mathematical range (e.g., m > 1).
