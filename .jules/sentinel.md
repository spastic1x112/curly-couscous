## 2025-05-14 - MT19937 State Reconstruction Validation
**Vulnerability:** Memory-exhaustion DoS and potential OverflowError in random.setstate().
**Learning:** Python's random.setstate() for MT19937 accepts integers up to the size of C's unsigned long (64-bit on many systems), but the algorithm expects 32-bit values. Providing values outside this range can lead to incorrect behavior or OverflowError. Additionally, reading unlimited input from files to collect state values can lead to DoS.
**Prevention:** Strictly validate that input values for MT19937 are 32-bit unsigned integers (0 to 2^32-1) and limit the number of values read from external files to the required amount (624 for MT19937).

## 2025-05-15 - Information Leakage and DoS in CLI File Reading
**Vulnerability:** CLI tool leaked sensitive file content in error messages and was vulnerable to memory-exhaustion DoS via extremely long lines in input files.
**Learning:** Default Python exceptions (like `ValueError` from `int()`) often echo the invalid input, which can be sensitive if the input comes from a file. Additionally, `for line in f` can exhaust memory if a file has no newlines.
**Prevention:** Use `raise ... from None` to suppress exception context when re-raising, and use `f.readline(limit)` to bound memory usage when reading potentially untrusted files. Wrap the CLI entry point in a generic try-except to prevent stack trace leakage.

## 2026-01-29 - LCG Parameter Validation and DoS Protection
**Vulnerability:** Unexpected execution paths via truthy checks and memory-exhaustion DoS in LCG cracking.
**Learning:** Using truthy checks (`if arg:`) for numeric parameters in a CLI can lead to incorrect behavior when 0 is a valid input (e.g., LCG increment `c=0`). Additionally, processing unlimited historical states for LCG parameter recovery can lead to DoS.
**Prevention:** Always use explicit `is not None` checks for optional numeric CLI arguments. Limit the number of historical states processed in cryptanalytic functions like `crack_lcg` to a reasonable maximum (e.g., 100) and validate that the recovered modulus `m` is greater than 1.
