# RNG Decipherer

A tool to predict and crack common Pseudo-Random Number Generators (PRNGs).

## Features

- **MT19937 (Mersenne Twister)**: Reconstructs the internal state from 624 observed 32-bit outputs. This is the default generator used in Python's `random` module.
- **LCG (Linear Congruential Generator)**: Recovers parameters $a$, $c$, and $m$ from observed outputs and predicts the next value.

## Installation

```bash
pip install .
```

## Usage

### MT19937

```bash
rng-decipherer mt19937 --values <list of 624 32-bit integers>
```

### LCG

```bash
rng-decipherer lcg --values <list of at least 6 integers>
```

If parameters $a$, $c$, and $m$ are known:

```bash
rng-decipherer lcg --values <last_value> --a 1103515245 --c 12345 --m 2147483648
```
