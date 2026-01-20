## 2025-05-15 - [MT19937 State Validation]
**Vulnerability:** Lack of input validation for MT19937 observed values leads to `OverflowError` in `random.setstate()`.
**Learning:** Python's `random.setstate()` for MT19937 requires a tuple of exactly 624 32-bit unsigned integers. Providing values outside this range causes a crash in the underlying C implementation.
**Prevention:** Always validate that values fed into `MT19937Predictor` are within the range `[0, 2**32 - 1]`.
