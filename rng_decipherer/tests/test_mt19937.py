import random
from rng_decipherer.mt19937 import MT19937Predictor


def test_mt19937_prediction():
    # Use a fixed seed for reproducibility in tests
    r = random.Random(42)

    # Get 624 values to reconstruct the state
    values = [r.getrandbits(32) for _ in range(624)]

    predictor = MT19937Predictor()
    for v in values:
        predictor.feed(v)

    predicted_gen = predictor.get_random_instance()

    # Verify next 100 values
    for _ in range(100):
        assert predicted_gen.getrandbits(32) == r.getrandbits(32)


def test_mt19937_invalid_input():
    predictor = MT19937Predictor()

    # Test negative value
    try:
        predictor.feed(-1)
    except ValueError as e:
        assert "not a valid 32-bit unsigned integer" in str(e)
    else:
        assert False, "Should have raised ValueError for negative value"

    # Test too large value
    try:
        predictor.feed(0x100000000)
    except ValueError as e:
        assert "not a valid 32-bit unsigned integer" in str(e)
    else:
        assert False, "Should have raised ValueError for value > 32-bit"

    # Test non-integer
    try:
        predictor.feed("not an int")
    except ValueError as e:
        # This might be from the isinstance check I added
        assert "not a valid 32-bit unsigned integer" in str(e)
    else:
        assert False, "Should have raised ValueError for non-integer"


if __name__ == "__main__":
    test_mt19937_prediction()
    test_mt19937_invalid_input()
    print("MT19937 tests passed!")
