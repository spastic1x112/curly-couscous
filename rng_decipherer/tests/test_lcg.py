from rng_decipherer.lcg import LCGPredictor, crack_lcg


def test_lcg_cracking():
    # Parameters for a simple LCG
    a = 1103515245
    c = 12345
    m = 2**31

    # Generate some states
    states = [42]
    for _ in range(10):
        states.append((a * states[-1] + c) % m)

    # Try to crack it
    cracked_a, cracked_c, cracked_m = crack_lcg(states[:6])

    assert cracked_a == a
    assert cracked_c == c
    assert cracked_m == m

    predictor = LCGPredictor(a=cracked_a, c=cracked_c, m=cracked_m)
    predictor.feed(states[5])
    assert predictor.predict_next() == states[6]


if __name__ == "__main__":
    test_lcg_cracking()
    print("LCG test passed!")
