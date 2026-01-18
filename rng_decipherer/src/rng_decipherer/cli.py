import argparse
import sys
from rng_decipherer.mt19937 import MT19937Predictor
from rng_decipherer.lcg import LCGPredictor, crack_lcg

def main():
    parser = argparse.ArgumentParser(description="RNG Decipherer Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # MT19937 command
    mt_parser = subparsers.add_parser("mt19937", help="Predict MT19937 (e.g. Python's random)")
    mt_parser.add_argument("--values", nargs="+", type=int, help="Sequence of 624 32-bit integers")
    mt_parser.add_argument("--file", type=str, help="File containing sequence of 32-bit integers (one per line)")

    # LCG command
    lcg_parser = subparsers.add_parser("lcg", help="Predict/Crack LCG")
    lcg_parser.add_argument("--values", nargs="+", type=int, help="Sequence of integers")
    lcg_parser.add_argument("--a", type=int, help="Multiplier 'a'")
    lcg_parser.add_argument("--c", type=int, help="Increment 'c'")
    lcg_parser.add_argument("--m", type=int, help="Modulus 'm'")

    args = parser.parse_args()

    if args.command == "mt19937":
        values = []
        if args.values:
            values = args.values
        elif args.file:
            with open(args.file, 'r') as f:
                values = [int(line.strip()) for line in f if line.strip()]

        if len(values) < 624:
            print(f"Error: MT19937 requires 624 values, only got {len(values)}.")
            sys.exit(1)

        predictor = MT19937Predictor()
        for v in values[:624]:
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
            print(f"Predicting next value with known parameters: {predictor.predict_next()}")
        else:
            print("Attempting to crack LCG parameters...")
            try:
                a, c, m = crack_lcg(args.values)
                print(f"Cracked Parameters: a={a}, c={c}, m={m}")
                predictor = LCGPredictor(a=a, c=c, m=m)
                predictor.feed(args.values[-1])
                print(f"Next predicted value: {predictor.predict_next()}")
            except Exception as e:
                print(f"Failed to crack LCG: {e}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
