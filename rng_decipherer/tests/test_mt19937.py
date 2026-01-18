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

if __name__ == "__main__":
    test_mt19937_prediction()
    print("MT19937 test passed!")
