# Sentinel Security Journal

## 2025-05-14 - DoS Risk and Information Leakage in CLI
**Vulnerability:** The CLI tool read entire files into memory before processing, leading to potential Denial-of-Service (DoS) via memory exhaustion. Additionally, stack traces and file contents were leaked in error messages.
**Learning:** Even simple CLI tools can be vulnerable to DoS if they don't limit input sizes. Python's default error messages for `int()` conversion can leak the exact string that failed to parse, which might be sensitive data from a file.
**Prevention:** Always limit file reads to the required amount and use generic error messages with top-level exception handling to suppress stack traces in production-ready tools.
