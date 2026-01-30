## 2025-05-14 - MT19937 State Reconstruction Validation
**Vulnerability:** Memory-exhaustion DoS and potential OverflowError in random.setstate().
**Learning:** Python's random.setstate() for MT19937 accepts integers up to the size of C's unsigned long (64-bit on many systems), but the algorithm expects 32-bit values. Providing values outside this range can lead to incorrect behavior or OverflowError. Additionally, reading unlimited input from files to collect state values can lead to DoS.
**Prevention:** Strictly validate that input values for MT19937 are 32-bit unsigned integers (0 to 2^32-1) and limit the number of values read from external files to the required amount (624 for MT19937).

## 2025-05-15 - Information Leakage and DoS in CLI File Reading
**Vulnerability:** CLI tool leaked sensitive file content in error messages and was vulnerable to memory-exhaustion DoS via extremely long lines in input files.
**Learning:** Default Python exceptions (like `ValueError` from `int()`) often echo the invalid input, which can be sensitive if the input comes from a file. Additionally, `for line in f` can exhaust memory if a file has no newlines.
**Prevention:** Use `raise ... from None` to suppress exception context when re-raising, and use `f.readline(limit)` to bound memory usage when reading potentially untrusted files. Wrap the CLI entry point in a generic try-except to prevent stack trace leakage.

## 2025-05-16 - LCG Parameter Validation and DoS Protection
**Vulnerability:** LCG cracking was vulnerable to CPU/memory exhaustion with large inputs, and the CLI incorrectly handled 0 as an LCG parameter.
**Learning:** Using truthiness checks (e.g., `if args.a`) for numeric parameters can lead to bugs when 0 is a valid value. Mathematical algorithms like LCG cracking should have input limits to prevent DoS from untrusted or overly large datasets.
**Prevention:** Use explicit `is not None` checks for numeric CLI arguments. Limit the number of observed states used in cracking algorithms (e.g., to the first 100). Validate that the recovered modulus `m` is greater than 1 to avoid degenerate cases.
