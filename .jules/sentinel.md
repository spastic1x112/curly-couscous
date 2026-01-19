## 2025-05-14 - MT19937 State Overflow
**Vulnerability:** Lack of input validation on MT19937 outputs allows for `OverflowError` when reconstructing state using Python's `random.setstate()`.
**Learning:** Python's `random.setstate()` expects a specific internal state format, and providing integers larger than what the underlying C implementation expects (usually 32-bit for MT19937) causes a crash.
**Prevention:** Always validate that inputs to PRNG reconstruction tools match the expected range of the PRNG (e.g., 0 to 2^32-1 for MT19937).
