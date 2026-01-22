import argparse
import sys
from rng_decipherer.mt19937 import MT19937Predictor
from rng_decipherer.lcg import LCGPredictor, crack_lcg


def run_cli():
    parser = argparse.ArgumentParser(description="RNG Decipherer Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # MT19937 command
    mt_parser = subparsers.add_parser(
        "mt19937", help="Predict MT19937 (e.g. Python's random)"
    )
    mt_parser.add_argument(
        "--values", nargs="+", type=int, help="Sequence of 624 32-bit integers"
    )
    mt_parser.add_argument(
        "--file",
        type=str,
        help="File containing sequence of 32-bit integers (one per line)",
    )

    # LCG command
    lcg_parser = subparsers.add_parser("lcg", help="Predict/Crack LCG")
    lcg_parser.add_argument(
        "--values", nargs="+", type=int, help="Sequence of integers"
    )
    lcg_parser.add_argument("--a", type=int, help="Multiplier 'a'")
    lcg_parser.add_argument("--c", type=int, help="Increment 'c'")
    lcg_parser.add_argument("--m", type=int, help="Modulus 'm'")

    args = parser.parse_args()

    if args.command == "mt19937":
        values = []
        if args.values:
            values = args.values
        elif args.file:
            # Security: Limit file read to prevent memory exhaustion (DoS)
            # and use generic error messages to avoid leaking file content.
            try:
                with open(args.file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                values.append(int(line))
                            except ValueError:
                                raise ValueError(
                                    "Invalid integer value found in file"
                                ) from None
                            if len(values) >= 624:
                                break
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {args.file}") from None
            except ValueError:
                raise
            except Exception:
                raise Exception("An error occurred while reading the file") from None

        if len(values) < 624:
            print(f"Error: MT19937 requires 624 values, only got {len(values)}.")
            sys.exit(1)

        predictor = MT19937Predictor()
        for v in values[:624]:
            if not (0 <= v < 0x100000000):
                raise ValueError(f"Value {v} is out of 32-bit range.")
            predictor.feed(v)

        gen = predictor.get_random_instance()
        print("Reconstructed state successfully.")
        print(f"Next 10 predicted 32-bit values:")
        for _ in range(10):
            print(gen.getrandbits(32))

    elif args.command == "lcg":
        if not args.values:
            print("Error: --values is required for LCG.")
            sys.exit(1)

        if args.a and args.c and args.m:
            predictor = LCGPredictor(a=args.a, c=args.c, m=args.m)
            predictor.feed(args.values[-1])
            print(
                f"Predicting next value with known parameters: {predictor.predict_next()}"
            )
        else:
            print("Attempting to crack LCG parameters...")
            try:
                a, c, m = crack_lcg(args.values)
                print(f"Cracked Parameters: a={a}, c={c}, m={m}")
                predictor = LCGPredictor(a=a, c=c, m=m)
                predictor.feed(args.values[-1])
                print(f"Next predicted value: {predictor.predict_next()}")
            except Exception as e:
                # Security: use generic error message for cracking failures
                print(
                    f"Failed to crack LCG: Parameters could not be recovered from provided values."
                )

    elif args.command is None:
        parser.print_help()


def main():
    try:
        run_cli()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        # Security: Generic error handling to avoid leaking stack traces
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
