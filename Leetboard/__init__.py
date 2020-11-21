from .keyboard import Keyboard
from .patternrandom import PatternRandom

UNIVERSAL_SEED = PatternRandom([False, True, True, False, True, False, True, False])
def generate_pattern(length, items):
    UNIVERSAL_SEED.calls = 0

    if isinstance(items, float) or isinstance(items, int): items = list(range(int(items)))

    # set length of items to be greater than desired length
    items = items * (1 + int(length/len(items)))
    out = [None] * length
    
    i = 0
    while None in out:
        # select the first None space
        while out[i  % len(out)] != None: i += 1

        # add the first element to it if the pattern so demands
        if UNIVERSAL_SEED.next(): out[i % len(out)] = items.pop()

        # increment i and repeat
        i += 1
    
    UNIVERSAL_SEED.calls = 0
    return out